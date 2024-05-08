from UtilityLib import ProjectManager

class CoreBase(ProjectManager):
  settings = None
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def process(self, *args, **kwargs):
    self.update_attributes(self, kwargs)
    if self.settings.base.path_base:
      self.path_base = self.settings.base.path_base

    for _plugin_name, _PluginClass in (self.settings.exe.plugins[self.process_type] or {}).items():
      self.settings.plugin_data[_plugin_name] = _PluginClass(path_base=self.path_base, settings=self.settings)
      self.settings.plugin_data[_plugin_name].boot()
      self.settings.plugin_data[_plugin_name].run()
      self.settings.plugin_data[_plugin_name].shutdown()

