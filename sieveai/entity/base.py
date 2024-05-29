from ..plug import DictConfig

class MoleculeBase(DictConfig):
  def __init__(self, *args, **kwargs):
    self.update(kwargs)
