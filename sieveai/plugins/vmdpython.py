
from .base import PluginBase

class VMDPython(PluginBase):
  is_ready = False
  plugin_name = "VMD Python"
  process = ['analysis', 'helper', 'conversion']
  url = "https://vmd.robinbetz.com/"
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def setup(self, *args, **kwargs):
    self.update_attributes(self, kwargs)

  def boot(self, *args, **kwargs):
    ...

  def run(self, *args, **kwargs):
    ...

  def shutdown(self, *args, **kwargs):
    ...
