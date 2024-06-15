
from ..plug import StepManager, DictConfig
from ..managers import Structures
from ..managers.plugin import PluginManager
from .base import PluginBase

from Bio.PDB import PDBParser
from Bio.PDB.PDBExceptions import PDBConstructionWarning
import warnings as WARNINGS

# Python binding for AutoDock VINA
from vina import Vina as VinaPy

class Vina(PluginBase):
  is_ready = False
  plugin_name = "AutoDock VINA"
  plugin_uid = "Vina123"
  process = ['docking']
  url = "https://autodock-vina.readthedocs.io/en/latest/docking_python.html"

  Vina_config = None

  _max_conformers = 3

  path_vina_exe = None

  def __init__(self, *args, **kwargs):
    WARNINGS.simplefilter('ignore', PDBConstructionWarning)
    super().__init__(**kwargs)

  def _restore_progress(self, *args, **kwargs):
    if self.path_pkl_progress.exists():
      _ci = self.unpickle(self.path_pkl_progress)
      self.Complexes = _ci

    if self.path_pkl_molecules.exists():
      self.Receptors, self.Ligands = self.unpickle(self.path_pkl_molecules)

  def _update_progress(self, *args, **kwargs):
    if hasattr(self, 'Complexes'):
      self.pickle(self.path_pkl_progress, self.Complexes)

    if hasattr(self, 'Receptors') and hasattr(self, 'Ligands'):
      self.pickle(self.path_pkl_molecules, (self.Receptors, self.Ligands))

  def _set_defualt_config(self):

    self.Vina_config = DictConfig()

    self.Vina_config.default = {
        "exhaustiveness": 16,
        "verbosity": 2,
        "center_x": None,
        "center_y": None,
        "center_z": None,
        "size_x": None,
        "size_y": None,
        "size_z": None,
        "out": None,
        "cpu": None,
        "log": None,
        "seed": 41103333,
        "num_modes": 10,
      }

    self.Vina_config.other.spacing = 1
    self.Vina_config.other.residues = []

    self.Vina_config.energy_range = 3

    self.Vina_config.allowed_keys = ["flex", "receptor", "ligand",
                  "center_x", "center_y", "center_z",
                  "size_x", "size_y", "size_z",
                  "out", "log",
                  "cpu", "seed", "verbosity",
                  "exhaustiveness", "num_modes", "energy_range"]

  def _run_docking(self, cuid):
    """Runs vina command."""
    _cuid_c = self.Complexes[cuid]
    _config = {
            "--receptor": _cuid_c.path_receptor,
            "--ligand": _cuid_c.path_ligand,
            "--config": _cuid_c.path_vina_config,
            "--out": _cuid_c.path_out,
            "--verbosity": self.Vina_config.default.get('verbosity', 2),
            "cwd": _cuid_c.path_docking,
            ">": _cuid_c.path_log # from command line to file
          }
    self.cmd_run(self.path_vina_exe, **_config)

  def _run_api_docking(self, cuid):
    _vna = VinaPy(sf_name='vina')
    _cuid_c = self.Complexes[cuid]
    _vna.set_receptor(str(_cuid_c.path_receptor))

    _vna.set_ligand_from_file(str(_cuid_c.path_ligand))
    _vna.compute_vina_maps(center=_cuid_c.center, box_size=_cuid_c.box_size)

    # Score the current pose
    energy = _vna.score()
    print('Score before minimization: %.3f (kcal/mol)' % energy[0])

    # Minimized locally the current pose
    energy_minimized = _vna.optimize()
    print('Score after minimization : %.3f (kcal/mol)' % energy_minimized[0])
    _vna.write_pose(str(_cuid_c.path_ligand).with_suffix('.min.pdbqt'), overwrite=True)

    # Dock the ligand
    _vna.dock(exhaustiveness=32, n_poses=20)
    _vna.write_poses(str(_cuid_c.path_out), n_poses=5, overwrite=True)

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
    self.path_pkl_molecules = (self.path_base / 'docking' / self.plugin_uid).with_suffix('.Structures.sob')
    self.path_pkl_progress = (self.path_base / 'docking' / self.plugin_uid).with_suffix('.config.sob')
    self.path_excel_results = (self.path_base / self.plugin_uid ).with_suffix('.Results.xlsx')

    self.path_vina_exe = self.which('vina')
    self._restore_progress()

    self._set_defualt_config()

    self._steps_map_methods = {
      "init": self._prepare_molecules,
      "config": self._write_receptor_vina_config,
      # "dock": self._run_docking,
      # "dock": self._run_api_docking,
      "extract": self._run_extraction,
      "analyse": self._run_analysis,
      "final": self._finalise_complex,
    }

    self._step_sequence = tuple(self._steps_map_methods.keys())

    if not self.path_pkl_molecules.exists():
      self.Receptors = Structures(self.SETTINGS.user.path_receptors, '*.pdb', 'macromolecule')
      self.Ligands = Structures(self.SETTINGS.user.path_ligands, '*.pdb', 'compound')
      self.log_debug('Storing Molecules')
      self._update_progress()

      # Check files have changed by comparing mol_path.hash == mol_hash
      # If changed re-read the molecule
      # Validate structure directory hash if anything changed
      # If changed re-read the molecule(s)

    else:
      self.log_debug('Restoring Molecules')

    if not self.path_pkl_progress.exists():
      self.Complexes = self.ObjDict()

  def _process_complex(self, cuid) -> None:
    if not cuid in self.Complexes:
      return

    for _step in self.Complexes[cuid].step:
      if _step in self.Complexes[cuid].steps_completed:
        continue

      _step = self.Complexes[cuid].step._current

      if self.Complexes[cuid].step.is_last:
        self.log_debug(f"{cuid}:: Last Step: {_step}")
      else:
        self.log_debug(f"{cuid}:: Step: {_step}")

      self._steps_map_methods[_step](cuid)
      self.Complexes[cuid].steps_completed.append(_step)
      self._update_progress()

  _vina_exe = None
  multiprocessing = False
  def _queue_complexes(self) -> None:
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

        # Convert mol_path to PDBQT using meeko/OpenBabel???

        _c_rec = _complex_path / f'REC.pdbqt'
        _c_lig = _complex_path / f'LIG.pdbqt'

        _rec.mol_path_pdbqt.copy(_c_rec)
        _lig.mol_path_pdbqt.copy(_c_lig)

        self.Complexes[_complex_uid].update({
            "step": StepManager(self._step_sequence),
            "steps_completed": [],
            "uid": _complex_uid,
            "rec_uid": _rec.mol_id,
            "lig_uid": _lig.mol_id,
            "path_receptor": _c_rec,
            "path_ligand": _c_lig,
            "path_docking": _complex_path,
            "path_out": _complex_path / f'{_complex_uid}.out.pdbqt',
            "path_log": _complex_path / f'{_complex_uid}.log',
          })

        self.log_debug(f'{_complex_uid}:: Queued.')

      if self.multiprocessing:
        self.queue_task(self._process_complex, _complex_uid)
      else:
        self._process_complex(_complex_uid)

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

  def _write_receptor_vina_config(self, cuid):
    if not cuid in self.Complexes:
      return

    _complx = self.Complexes[cuid]
    self.log_error('cmplx', _complx)

    if 'path_vina_config' in _complx and _complx.path_vina_config.exists() and _complx.path_vina_config.size > 0:
      self.log_info(f'{cuid} vina config file already exists. Skipping...')
      return
    else:
      self.Complexes[cuid].path_vina_config = _complx.path_docking / f"{cuid}.vina.config"

    _config_path = self.Complexes[cuid].path_vina_config

    _mol_obj = self.Receptors[_complx.rec_uid]

    _Parser = PDBParser(get_header=False)
    _structure = _Parser.get_structure(_mol_obj.mol_id, _mol_obj.mol_path)

    _coordinates = []

    # If config settings has specific residues for site specific docking then prepare grid around specific residues
    if self.Vina_config.other.get("residues") and len(self.Vina_config.other.get("residues")):
      for _chains in _structure.get_chains():
        for _chain in _chains:
          _chain_vars = vars(_chain)
          if _chain_vars.get("resname") in self.Vina_config.other.get("residues"):
            _coordinates.extend([[k for k in res.get_coord()] for res in _chain])
    else:
      _coordinates = [_atom.get_coord() for _atom in _structure.get_atoms()]

    # Calculate center, size, and distance
    _coord_x, _coord_y, _coord_z = zip(*_coordinates) if _coordinates else ([], [], [])

    _center = (sum(_coord_x) / len(_coord_x), sum(_coord_y) / len(_coord_y), sum(_coord_z) / len(_coord_z))

    _size = (max(_coord_x) - min(_coord_x), max(_coord_y) - min(_coord_y), max(_coord_z) - min(_coord_z))

    # Prepare VINA config
    _center_x, _center_y, _center_z = (round(_coord, 4) for _coord in _center)
    _size_x, _size_y, _size_z = (min(int(dim), 126) for dim in _size)

    _spacing = float(self.Vina_config.other.get("spacing", 1))

    _vina_config = {
        **self.Vina_config.default,
        "center_x": _center_x,
        "center_y": _center_y,
        "center_z": _center_z,
        "size_x": _size_x + _spacing,
        "size_y": _size_y + _spacing,
        "size_z": _size_z + _spacing,
      }

    self.Complexes[cuid].center = [_center_x, _center_y, _center_z]
    self.Complexes[cuid].box_size = [_size_x + _spacing, _size_y + _spacing, _size_z + _spacing]

    _vina_config = {_k: _vina_config[_k] for _k in _vina_config if _k in self.Vina_config.allowed_keys}

    _vina_config_lines = [f"{config_key} = {_vina_config[config_key]}" for config_key in _vina_config.keys() if _vina_config[config_key] is not None]

    _vina_config_lines = "\n".join(_vina_config_lines + ["\n"])

    _config_path.write(_vina_config_lines)

  def run(self, *args, **kwargs):
    # Setting molecular formats
    _mgltools = PluginManager.share_plugin('mgltools')()
    self.Receptors.set_format('pdbqt', converter=_mgltools.prepare_receptor)

    _openBabel = PluginManager.share_plugin('openbabel')()
    self.Ligands.set_format('pdbqt', converter=_openBabel.convert)

    self._queue_complexes()

    self._update_progress()

    # self.process_queue()
    # self.queue_final_callback(self._tabulate_results)

  def shutdown(self, *args, **kwargs):
    ...
