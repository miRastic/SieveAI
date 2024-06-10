from ..plug import SieveAIBase

class CoreBase(SieveAIBase):
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def process(self, *args, **kwargs):
    self.update_attributes(self, kwargs)
    if self.SETTINGS.user.path_base:
      self.path_base = self.SETTINGS.user.path_base

    for _plugin_name, _PluginClass in (self.SETTINGS.plugin_refs.docking or {}).items():
      if _plugin_name.startswith('_'):
        # ISSUE: DictConfig.__private_keys
        continue

      self.SETTINGS.plugin_data[_plugin_name] = _PluginClass(path_base=self.path_base, SETTINGS=self.SETTINGS)
      self.SETTINGS.plugin_data[_plugin_name].boot()
      self.SETTINGS.plugin_data[_plugin_name].run()
      self.SETTINGS.plugin_data[_plugin_name].shutdown()
