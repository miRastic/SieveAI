
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

  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def setup(self, *args, **kwargs):
    self.update_attributes(self, kwargs)

  def boot(self, *args, **kwargs):
    self.setup(*args, **kwargs)
    _rec = Structures(self.settings.base.path_receptors, '*.pdb', 'macromolecule')
    print('rec', len(_rec), _rec)
    _lig = Structures(self.settings.base.path_ligands, '*.pdb', 'macromolecule')
    print('rec', len(_lig), _lig)

  def _arrange_rec_lig_dirs(self):
    # Pre-process or cleaning of molecules
    # Create Directories and Copy Molecules
    # Perform docking and extraction of conformers
    self.debug(f"Receptors: {self.Receptors}")
    self.debug(f"Ligands: {self.Ligands}")

  def _perform_docking(self):
    # _x = self.combinations(self.Receptors, self.Ligands)
    # print(_x)
    ...

  def run(self, *args, **kwargs):
    self._arrange_rec_lig_dirs()
    self._perform_docking()
    # Run hdock
    # Run hdockpl
    # _hdock_commands.extend([
    #     f"""echo "Processing {_cuid} {_idx}/{_total}           `(date +%F_%H:%M:%S)`" """,
    #     f"""cd {_cd_to} """,
    #     f"""hdock "{_cuid}-rec.pdb" "{_cuid}-lig.pdb" -out "{_cuid}.out" &> "{_cuid}.hdock.log" """,
    #     f"""hdockpl "{_cuid}.out" "complex.pdb" -nmax 100 -complex -chid -models &> "{_cuid}.hdockpl.log" """
    # ])

  def shutdown(self, *args, **kwargs):
    ...
