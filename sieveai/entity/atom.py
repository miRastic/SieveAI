from UtilityLib import ObjDict

class Atom(ObjDict):
  def __init__(self, *args, **kwargs):
    self.update(kwargs)

class Atoms(ObjDict):
  def __init__(self, *args, **kwargs):
    self.update(kwargs)
