from UtilityLib import ProjectManager

class CoreBase(ProjectManager):
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
