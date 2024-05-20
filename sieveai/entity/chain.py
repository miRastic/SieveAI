from UtilityLib import ObjDict

class Chain(ObjDict):
  def __init__(self, *args, **kwargs):
    self.update(kwargs)

class Chains(ObjDict):
  def __init__(self, *args, **kwargs):
    self.update(kwargs)
