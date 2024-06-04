from .base import ManagerBase
from .structure import Structures

class MoleculeManager(ManagerBase):
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def get_uniprot(self): pass

  def get_rcsb(self): pass

  def get_pubchem(self): pass
