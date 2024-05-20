from UtilityLib import ObjDict

class Residue(ObjDict):
  def __init__(self, *args, **kwargs):
    self.update(kwargs)

class Residues(ObjDict):
  def __init__(self, *args, **kwargs):
    self.update(kwargs)
