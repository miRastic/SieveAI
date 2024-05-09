from UtilityLib import ObjDict, UM

class MoleculeBase(ObjDict):
  UM = UM
  ObjDict = ObjDict
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
    self.update(kwargs)
