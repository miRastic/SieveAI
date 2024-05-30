
from .base import PluginBase
from ..managers import Structures

class HDockLite(PluginBase):
  is_ready = False
  plugin_name = "HDockLite"
  process = ['docking']
  url = "http://hdock.phys.hust.edu.cn/"
  MolManager = None
  Receptors = None
  Ligands = None

  _hdock_exe = None
  _hdock_exe_name = 'hdock'
  _hdock_exe_name_pl = 'hdockpl'
  path_results = None

  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def setup(self, *args, **kwargs):
    self.update_attributes(self, kwargs)

  def boot(self, *args, **kwargs):
    self.setup(*args, **kwargs)
    self.Receptors = Structures(self.settings.base.path_receptors, '*.pdb', 'macromolecule')
    self.Ligands = Structures(self.settings.base.path_ligands, '*.pdb', 'macromolecule')

  def _perform_docking(self, _rec, _lig):
    _complex = self.slug(f"{_rec.mol_id}--{_lig.mol_id}")
    _complex_path = (self.path_results / _complex).validate()

    _complex_log_path = _complex_path / f'{_complex}.log'

    self.log_info(f'Initiating-Docking {_rec.mol_id} {_lig.mol_id}')

    _c_rec = _complex_path / f'REC{_rec.mol_path.suffix}'
    _c_lig = _complex_path / f'LIG{_lig.mol_path.suffix}'

    _rec.mol_path.copy(_c_rec)
    _lig.mol_path.copy(_c_lig)

    self.OS.chdir(_complex_path)
    _log = self.cmd_run(self._hdock_exe, _c_rec.name, _c_lig.name, **{
      'out': f"{_complex}.out"
    })
    _complex_log_path.write(str(_log))
    _log = self.cmd_run(self._hdock_exe_name_pl, f"{_complex}.out", "complex.pdb", "-nmax 100 -complex -chid -models")
    _complex_log_path.write(str(_log))

    self.log_info(f'Docked-Complex {_rec.mol_id} {_lig.mol_id}')

  _is_multiprocess = True

  def _arrange_molecules(self):
    # Pre-process or cleaning of molecules
    # Create Directories and Copy Molecules
    # Perform docking and extraction of conformers
    self.debug(f"Receptors: {self.Receptors}")
    self.debug(f"Ligands: {self.Ligands}")

    self._hdock_exe = self.which(self._hdock_exe_name)
    self.path_results = (self.path_base / 'docking' / self.plugin_name).validate()

    if not self._hdock_exe:
      self.log_error(f'{self._hdock_exe_name} executable is not found. Please provide the executable command or path to executable file.')
      return

    self.init_multiprocessing()
    _combs = list(self.product([self.Receptors.keys(), self.Ligands.keys()], 1))
    for _rck, _ligk in self.PB(_combs):
      _rec = self.Receptors[_rck]
      _lig = self.Ligands[_ligk]
      if self._is_multiprocess:
        self.queue_task(self._perform_docking, _rec, _lig)
      else:
        self._perform_docking(_rec, _lig)

    self.process_queue()

  def run(self, *args, **kwargs):
    self._arrange_molecules()

  def shutdown(self, *args, **kwargs):
    ...
