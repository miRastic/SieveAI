
from .base import PluginBase
from ..managers import Structures

class FreeSASA(PluginBase):
  is_ready = False
  plugin_name = "FreeSASA"
  process = ['analysis']
  url = "https://freesasa.github.io/"

  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def setup(self, *args, **kwargs):
    self.update_attributes(self, kwargs)

  def boot(self, *args, **kwargs):
    self.setup(*args, **kwargs)


  def run(self, *args, **kwargs):
    ...

  def shutdown(self, *args, **kwargs):
    ...
