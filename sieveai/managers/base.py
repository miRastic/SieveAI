from UtilityLib import ProjectManager, ObjDict

class ManagerBase(ProjectManager):
  ObjDict = ObjDict
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
