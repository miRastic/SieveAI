from UtilityLib import ObjDict

class MoleculeBase(ObjDict):
  def __init__(self, *args, **kwargs):
    self.update(kwargs)
