
from .base import PluginBase
from ..managers.molecule import MoleculeManager

class Vina(PluginBase):
  MolManager = None
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
    self.MolManager = MoleculeManager(**kwargs)

  def setup(self, *args, **kwargs):
    self.update_attributes(self, kwargs)

  def boot(self, *args, **kwargs):
    self.setup(*args, **kwargs)
    _receptors = self.MolManager.get_molecules('path_receptors', 'pdb', 'protein')
    _ligands = self.MolManager.get_molecules('path_ligands', 'pdb', 'compound')

    print(_receptors, _ligands)
    ...

  def run(self, *args, **kwargs):
    ...

  def shutdown(self, *args, **kwargs):
    ...
