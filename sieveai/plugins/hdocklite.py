
from .base import PluginBase
from ..managers import MoleculeManager

class HDockLite(PluginBase):
  is_ready = False
  plugin_name = "HDockLite"
  url = "http://hdock.phys.hust.edu.cn/"
  MolManager = None
  Receptors = None
  Ligands = None
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
    self.MolManager = MoleculeManager(**kwargs)

  def setup(self, *args, **kwargs):
    self.update_attributes(self, kwargs)

  def boot(self, *args, **kwargs):
    self.setup(*args, **kwargs)
    self.Receptors = self.MolManager.get_molecules('path_receptors', '*.pdb', 'macromolecule')
    self.Ligands = self.MolManager.get_molecules('path_ligands', '*.pdb', 'macromolecule')

  def _arrange_rec_lig_dirs(self):
    # Pre-process or cleaning of molecules
    # Create Directories and Copy Molecules
    # Perform docking and extraction of conformers
    self.debug(f"Rec: {self.Receptors}")
    self.debug(f"Lig: {self.Ligands}")

  def run(self, *args, **kwargs):
    self._arrange_rec_lig_dirs()
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
