
from ..plug import StepManager
from ..managers import Structures
from .base import PluginBase

# Python binding for AutoDock VINA
from vina import Vina

class Vina(PluginBase):
  is_ready = False
  plugin_name = "AutoDock VINA"
  plugin_uid = "Vina123"
  process = ['docking']
  url = "https://autodock-vina.readthedocs.io/en/latest/docking_python.html"

  _max_conformers = 10

  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def _restore_progress(self, *args, **kwargs):
    if self.path_pkl_progress.exists():
      _ci = self.unpickle(self.path_pkl_progress)
      self.Complexes = _ci

  def _update_progress(self, *args, **kwargs):
    self.pickle(self.path_pkl_progress, self.Complexes)

  def _run_docking(self, cuid):
    """Runs hdock and hdockpl to perform docking and later extact the complexes.
    """
    # _log = self.cmd_run(self._hdock_exe_name, self.Complexes[cuid].REC.name, self.Complexes[cuid].LIG.name, **{
    #   'out': f"{cuid}.out",
    #   'cwd': self.Complexes[cuid].path_docking
    # })

    # self.Complexes[cuid].path_log.write(str(_log))

  def _run_extraction(self, cuid):

    pass

  def _run_analysis(self, cuid):
    return
    _VPY = self.SETTINGS.plugin_refs.analysis.vmdpython()

    *_models, = list(self.Complexes[cuid].path_docking.search('model*'))
    _models.sort(key=self._fn_sort_model)

    _model_results = []
    for _model in _models:
      _vmd_id = _VPY.parse_molecule(str(_model))
      _rec_obj = _VPY.get_atom_sel('chain A', _vmd_id)
      _lig_obj = _VPY.get_atom_sel('chain B', _vmd_id)

      _lines = list(_model._read_lines(num_lines=5))
      _remarks = dict([_r[0] for _r in map(self.re_remarks.findall, _lines)])
      _remarks['Complex_uid'] = cuid
      _interactions = _VPY.get_interactions(_rec_obj, _lig_obj)
      _remarks.update(_interactions)
      _model_results.append(_remarks)

    self.log_debug(f'{cuid}:: Conformer Results Generated')

    _df_conformer_scores = self.DF(_model_results)
    _df_conformer_scores['plugin'] = self.plugin_uid
    self.Complexes[cuid].conformer_scores = _df_conformer_scores

  def _prepare_molecules(self, cuid):
    return cuid

  def _finalise_complex(self, cuid):
    return cuid

  def boot(self, *args, **kwargs):
    self.update_attributes(self, kwargs)

    self.path_plugin_res = (self.path_base / 'docking' / self.plugin_uid).validate()
    self.path_pkl_molecules = (self.path_plugin_res / self.plugin_uid).with_suffix('.Structures.pkl.gz')
    self.path_pkl_progress = (self.path_plugin_res / self.plugin_uid).with_suffix('.pkl.gz')
    self.path_excel_results = (self.path_base / self.plugin_uid ).with_suffix('.Results.xlsx')
    self._restore_progress()

    self._steps_map_methods = {
      "init": self._prepare_molecules,
      "dock": self._run_docking,
      "extract": self._run_extraction,
      "analyse": self._run_analysis,
      "completed": self._finalise_complex,
    }

    self._step_sequence = tuple(self._steps_map_methods.keys())

    if self.path_pkl_molecules.exists():
      self.log_debug('Restoring Molecules')
      self.Receptors, self.Ligands = self.unpickle(self.path_pkl_molecules)

      # Check files have changed by comparing mol_path.hash == mol_hash
      # If changed re-read the molecule
      # Validate structure directory hash if anything changed
      # If changed re-read the molecule(s)

    else:
      self.Receptors = Structures(self.SETTINGS.user.path_receptors, '*.pdb', 'macromolecule')
      self.Ligands = Structures(self.SETTINGS.user.path_ligands, '*.pdb', 'compound')
      self.log_debug('Storing Molecules')
      self.pickle(self.path_pkl_molecules, (self.Receptors, self.Ligands))

    if self.path_pkl_progress.exists():
      self._restore_progress()
    else:
      self.Complexes = self.ObjDict()

  def _process_complex(self, cuid):
    if cuid in self.Complexes:
      for _step in self.Complexes[cuid].step:
        if _step in self.Complexes[cuid].steps_completed:
          continue

        _step = self.Complexes[cuid].step._current

        if self.Complexes[cuid].step.is_last:
          self.log_debug(f"{cuid}:: Last Step: {_step}")
        else:
          self.log_debug(f"{cuid}:: Step: {_step}")

        # self._steps_map_methods[_step](cuid)
        self.Complexes[cuid].steps_completed.append(_step)
        self._update_progress()

  _vina_exe = None
  def _queue_complexes(self):
    self.log_debug(f"Receptors: {self.Receptors}")
    self.log_debug(f"Ligands: {self.Ligands}")

    self._vina_exe = self.which('vina')

    if not self._vina_exe:
      self.log_error(f'{self._vina_exe} executable is not found. Please provide the executable command or path to executable file.')
      return

    # Perform Docking
    self.init_multiprocessing()
    _combs = list(self.product([self.Receptors.keys(), self.Ligands.keys()], 1))
    for _rck, _ligk in self.PB(_combs, desc='Queue'):
      _rec = self.Receptors[_rck]
      _lig = self.Ligands[_ligk]

      _complex_uid = self.slug(f"{_rec.mol_id}--{_lig.mol_id}")

      if not _complex_uid in self.Complexes:
        self.Complexes[_complex_uid] = self.ObjDict()

        _complex_path = (self.path_plugin_res / _complex_uid).validate()
        _complex_log_path = _complex_path / f'{_complex_uid}.log'

        # Copy _path
        _c_rec = _complex_path / f'REC{_rec.mol_path.suffix}'
        _c_lig = _complex_path / f'LIG{_lig.mol_path.suffix}'

        _rec.mol_path.copy(_c_rec)
        _lig.mol_path.copy(_c_lig)

        self.Complexes[_complex_uid].update({
            "step": StepManager(self._step_sequence),
            "steps_completed": [],
            "uid": _complex_uid,
            "REC": _c_rec,
            "LIG": _c_lig,
            "path_docking": _complex_path,
            "path_log": _complex_log_path,
          })

        self.log_debug(f'{_complex_uid}:: Queued.')

      if self.multiprocessing:
        self.queue_task(self._process_complex, _complex_uid)
      else:
        self._process_complex(_complex_uid)

    self._update_progress()
    self.process_queue()
    self.queue_final_callback(self._tabulate_results)

  _df_results = None
  def _tabulate_results(self, *args, **kwargs):
    while self.queue_running > 0:
      self.log_debug()
      self.time_sleep(30)

    return True

    self.require('pandas', 'PD')

    # Combine all the interactions
    _score_table = None
    for _idx, _cmplx in self.Complexes.items():
      if not isinstance(_cmplx, (dict)) or not 'conformer_scores' in _cmplx:
        continue

      if _score_table is None:
        _score_table = _cmplx.conformer_scores
      else:
        _score_table = self.PD.concat([_score_table, _cmplx.conformer_scores])

    # Save conformers and ranks as excel
    self._df_results, _top_ranked = self._rank_conformers(_score_table)
    self.pd_excel(self.path_excel_results, self._df_results, sheet_name=f"{self.plugin_uid}-All-Ranked")
    self.pd_excel(self.path_excel_results, _top_ranked, sheet_name=f"{self.plugin_uid}-Top-Ranked")


  def run(self, *args, **kwargs):
    self._queue_complexes()

  def shutdown(self, *args, **kwargs):
    ...
