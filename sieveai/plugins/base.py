from UtilityLib import ProjectManager

class PluginBase(ProjectManager):
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
