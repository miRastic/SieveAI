from UtilityLib import ObjDict

class MoleculeBase(ObjDict):
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
