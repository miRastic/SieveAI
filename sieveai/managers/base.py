from UtilityLib import ProjectManager

class ManagerBase(ProjectManager):
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
