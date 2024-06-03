
from .base import PluginBase
from ..managers import Structures
from ..plug import StepManager

class HDockLite(PluginBase):
  is_ready = False
  plugin_name = "HDockLite"
  process = ['docking']
  url = "http://hdock.phys.hust.edu.cn/"
  MolManager = None

  _max_conformers = 10

  _hdock_exe = None
  _hdock_exe_name = 'hdock'
  _hdock_exe_name_pl = 'hdockpl'

  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
    self.Complexes = self.ObjDict()

    self.Receptors = None
    self.Ligands = None

    self.path_table = None
    self.path_update = None

    self.path_plugin_res = (self.path_base / 'docking' / self.plugin_name).validate()
    self.path_update = (self.path_plugin_res / self.plugin_name).with_suffix('.pkl.gz')
    self._restore_progress()

    self._steps_map_methods = {
      "init": self._run_preprocess_check,
      "dock": self._run_hdock_main,
      "extract": self._run_hdock_pl,
      "analyse": self._run_analysis,
      "completed": self._finalise_complex,
    }

    self._step_sequence = tuple(self._steps_map_methods.keys())
    self.re_remarks = self.re_compile(r'REMARK\s(\w+):\s+(.*)$')

  def setup(self, *args, **kwargs):
    self.update_attributes(self, kwargs)

  def boot(self, *args, **kwargs):
    self.setup(*args, **kwargs)
    self.Receptors = Structures(self.settings.base.path_receptors, '*.pdb', 'macromolecule')
    self.Ligands = Structures(self.settings.base.path_ligands, '*.pdb', 'macromolecule')

  def _restore_progress(self, *args, **kwargs):
    if self.path_update.exists():
      _ci = self.unpickle(self.path_update)
      self.Complexes = _ci

  def _update_progress(self, *args, **kwargs):
    self.pickle(self.path_update, self.Complexes)

  def _run_hdock_main(self, cuid):
    """Runs hdock and hdockpl to perform docking and later extact the complexes.
    """
    _log = self.cmd_run(self._hdock_exe_name, self.Complexes[cuid].REC.name, self.Complexes[cuid].LIG.name, **{
      'out': f"{cuid}.out",
      'cwd': self.Complexes[cuid].path_docking
    })

    self.Complexes[cuid].path_log.write(str(_log))

  def _run_hdock_pl(self, cuid):
    """Runs hdock and hdockpl to perform docking and later extact the complexes.
    """
    _log = self.cmd_run(self._hdock_exe_name_pl, f"{cuid}.out", "complex.pdb", "-nmax", self._max_conformers, "-complex", "-chid", "-models", cwd=self.Complexes[cuid].path_docking)

    self.Complexes[cuid].path_log.write(str(_log))

  def _fn_sort_model(self, _model_path=""):
    _number = self.digit_only(self.filename(_model_path))
    return int(_number)

  def _run_analysis(self, cuid):
    _VPY = self.settings.exe.plugin_refs.analysis.vmdpython()

    *_models, = list(self.Complexes[cuid].path_docking.search('model*'))
    _models.sort(key=self._fn_sort_model)

    _model_results = []
    for _model in _models:
      _vmd_id = _VPY.parse_molecule("pdb", str(_model))
      _rec_obj = _VPY.get_atom_sel('chain A', _vmd_id)
      _lig_obj = _VPY.get_atom_sel('chain B', _vmd_id)

      _lines = list(_model._read_lines(num_lines=5))
      _remarks = dict([_r[0] for _r in map(self.re_remarks.findall, _lines)])
      _remarks['Complex_uid'] = cuid
      _interactions = _VPY.get_interactions(_rec_obj, _lig_obj)
      _remarks.update(_interactions)
      _model_results.append(_remarks)

    self.log_debug(f'{cuid} Conformers Results')
    self.log_debug(_model_results)
    self.Complexes[cuid].conformer_interactions = self.DF(_model_results)
    self._update_progress()

  def _run_preprocess_check(self, cuid):
    """WIP"""

  def _finalise_complex(self, cuid):
    """WIP"""

  def status(self, cuid=None):
    _status = None
    if not cuid is None and cuid in self.Complexes:
      _status = self.Complexes[cuid].step.current
    else:
      _status = []
      for _idx, _item in self.Complexes.items():
        if not isinstance(_item, (dict)):
          continue

        _status.append((_idx, _item.step.current))

    return _status

  def _process_complex(self, cuid):
    if cuid in self.Complexes:
      for _step in self.Complexes[cuid].step:
        if _step in self.Complexes[cuid].steps_completed:
          continue

        _step = self.Complexes[cuid].step._current
        self.log_debug(f"Step: {_step}")

        self._steps_map_methods[_step](cuid)
        self.Complexes[cuid].steps_completed.append(_step)
        self._update_progress()

        if self.Complexes[cuid].step.is_last:
          self.log_debug(f"Last Step: {_step}")
          break

  _is_multiprocess = True

  def _queue_complexes(self):
    # Pre-process or cleaning of molecules
    # Create Directories and Copy Molecules
    # Perform docking and extraction of conformers
    self.debug(f"Receptors: {self.Receptors}")
    self.debug(f"Ligands: {self.Ligands}")

    self._hdock_exe = self.which(self._hdock_exe_name)

    self.path_table = self.path_plugin_res.with_suffix('.pkl.gz')

    if not self._hdock_exe:
      self.log_error(f'{self._hdock_exe_name} executable is not found. Please provide the executable command or path to executable file.')
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

        self.log_debug(f'Queued {_complex_uid}')

      if self._is_multiprocess:
        self.queue_task(self._process_complex, _complex_uid)
      else:
        self._process_complex(_complex_uid)

    self._update_progress()
    self.process_queue()

  def run(self, *args, **kwargs):
    self._queue_complexes()

  def shutdown(self, *args, **kwargs):
    # Check if all compounds are docked
    # Tabulate docking scores
    # Prepare summary of docking
    ...
