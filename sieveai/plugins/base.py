from ..base import SieveAIBase

class PluginBase(SieveAIBase):
  is_ready = False
  plugin_name = "Base"
  url = None
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def installation_instructions(self, *args, **kwargs):
    ...
