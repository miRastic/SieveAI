
from .base import PluginBase
from openbabel import openbabel as OBabel

class OpenBabel(PluginBase):
  is_ready = False
  plugin_name = "OpenBabel"
  process = ['conversion']
  url = "https://github.com/openbabel/openbabel"

  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def setup(self, *args, **kwargs):
    self.update_attributes(self, kwargs)

  def convert_string(self, *args, **kwargs):
    _source_text = args[0] if len(args) > 0 else kwargs.get('path_source')
    _path_target = args[0] if len(args) > 0 else kwargs.get('path_target')

    _format_to = args[1] if len(args) > 1 else kwargs.get('format_to')
    _format_from = args[2] if len(args) > 2 else kwargs.get('format_from')
    _addh = args[3] if len(args) > 3 else kwargs.get('addh', False)

    # Check if to and from formats are valid for OpenBabel
    _obc = OBabel.OBConversion()
    _obc.SetInAndOutFormats(_format_from, _format_to)

    _mol = OBabel.OBMol()
    # Open Babel will uncompress .gz files automatically
    _obc.ReadString(_mol, _source_text)

    # Optionally add hydrogens
    if _addh:
      _mol.AddHydrogens()

    _obc.WriteFile(_mol, _path_target)

  def convert(self, *args, **kwargs):
    _path_source = kwargs.get('path_source', args[0] if len(args) > 0 else None)
    _path_target = kwargs.get('path_target', args[1] if len(args) > 1 else None)

    _format_to = kwargs.get('format_to', args[2] if len(args) > 2 else _path_source.suffix)
    _format_from = kwargs.get('format_from', args[3] if len(args) > 3 else _path_target.suffix)

    _addh = kwargs.get('addh', args[4] if len(args) > 4 else False)

    # Check if to and from formats are valid for OpenBabel
    _obc = OBabel.OBConversion()
    _obc.SetInAndOutFormats(_format_from, _format_to)

    _mol = OBabel.OBMol()
    # Open Babel will uncompress .gz files automatically
    _obc.ReadFile(_mol, str(_path_source))

    # Optionally add hydrogens
    if _addh:
      _mol.AddHydrogens()

    _obc.WriteFile(_mol, str(_path_target))
