from .molecule import Molecule

class Compound(Molecule):
  def __init__(self, *args, **kwargs):
    _defaults = {
      'mol_cat': 'compound',
    }
    _defaults.update(kwargs)
    self.update(_defaults)
