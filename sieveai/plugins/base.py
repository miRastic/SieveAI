from UtilityLib import ProjectManager

class PluginBase(ProjectManager):
  is_ready = False
  plugin_name = "Base"
  url = None
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def installation_instructions(self, *args, **kwargs):
    ...
