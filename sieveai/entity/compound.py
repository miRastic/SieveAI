from .molecule import Molecule

class Compound(Molecule):
  def __init__(self, *args, **kwargs):
    self.mol_type = 'compound'
    super().__init__(**kwargs)
