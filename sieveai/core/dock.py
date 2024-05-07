from .base import CoreBase
from ..managers.plugin import PluginManager

class Dock(CoreBase):
  settings = None
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def process(self, *args, **kwargs):
    self.update_attributes(self, kwargs)
    if self.settings.base.path_base:
      self.path_base = self.settings.base.path_base

    if not self.settings.base.path_project:
      self.settings.base.path_project = self.settings.base.path_base

    for _PluginClass in self.settings.exe.plugins.docking or []:
      _plugin = _PluginClass(settings=self.settings)
      _plugin.setup()
      _plugin.boot()
      _plugin.run()
      _plugin.shutdown()