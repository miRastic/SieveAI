from .base import PluginBase

class AnnapuRNA(PluginBase):
  is_ready = False
  plugin_name = "AnnapuRNA"
  process = ['rescoring']
  url = "https://github.com/filipsPL/annapurna"

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
