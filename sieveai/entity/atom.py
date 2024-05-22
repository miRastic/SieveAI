from ..base import DictConfig

class Atom(DictConfig):
  def __init__(self, *args, **kwargs):
    self.update(kwargs)

class Atoms(DictConfig):
  def __init__(self, *args, **kwargs):
    self.update(kwargs)
