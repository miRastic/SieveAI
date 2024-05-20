
from .base import PluginBase
from ..managers import MoleculeManager

from vina import Vina # Python binding for AutoDock VINA

class Vina(PluginBase):
  is_ready = False
  plugin_name = "AutoDock VINA"
  url = "https://autodock-vina.readthedocs.io/en/latest/docking_python.html"
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
    self.Receptors = self.MolManager.get_molecules('path_receptors', 'pdb', 'protein')
    self.Ligands = self.MolManager.get_molecules('path_ligands', 'pdb', 'compound')

  def _prepare_receptor(self, _rec_id):
    self.Receptors[_rec_id].to_format('pdbqt')


  def run(self, *args, **kwargs):
    for _mol_id, _mol_obj in self.Receptors:
      self._prepare_receptor(_mol_id)
    ...

  def shutdown(self, *args, **kwargs):
    ...
