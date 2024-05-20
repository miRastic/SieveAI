
from .base import PluginBase

class ChimeraX(PluginBase):
  is_ready = False
  plugin_name = "ChimeraX"
  url = "https://www.cgl.ucsf.edu/chimerax/docs/user/index.html"
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
