from .base import MoleculeBase
from .atom import Atoms

class Molecule(MoleculeBase):
  def __init__(self, *args, **kwargs):
    _defaults = {
      'n_atoms': None,
      '_atoms': Atoms(),
    }
    _defaults.update(kwargs)
    self.update(_defaults)
