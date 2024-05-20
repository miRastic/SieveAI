
from .base import PluginBase
from openbabel import openbabel as OBabel

class Meeko(PluginBase):
  is_ready = False
  plugin_name = "Meeko"
  url = "https://github.com/forlilab/Meeko"
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def setup(self, *args, **kwargs):
    self.update_attributes(self, kwargs)

  def convert(self, *args, **kwargs):
    _path_source = kwargs.get('path_source', args[0] if len(args) > 0 else None)
    _path_destination = kwargs.get('path_destination', args[1] if len(args) > 1 else None)

    _format_to = args[2] if len(args) > 2 else kwargs.get('format_to')
    _format_from = args[3] if len(args) > 3 else kwargs.get('format_from')
    _addh = args[4] if len(args) > 4 else kwargs.get('addh', True)
