
from .base import PluginBase
from openbabel import openbabel as OBABEL

class OpenBabel(PluginBase):
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

  def convert_string(self, *args, **kwargs):
    _source_text = args[0] if len(args) > 0 else kwargs.get('path_source')
    _path_destination = args[0] if len(args) > 0 else kwargs.get('path_destination')

    _format_to = args[1] if len(args) > 1 else kwargs.get('format_to')
    _format_from = args[2] if len(args) > 2 else kwargs.get('format_from')
    _addh = args[3] if len(args) > 3 else kwargs.get('addh', False)

    # Check if to and from formats are valid for OpenBabel
    _obc = OBABEL.OBConversion()
    _obc.SetInAndOutFormats(_format_from, _format_to)

    _mol = OBABEL.OBMol()
    # Open Babel will uncompress .gz files automatically
    _obc.ReadString(_mol, _source_text)

    # Optionally add hydrogens
    if _addh:
      _mol.AddHydrogens()

    _obc.WriteFile(_mol, _path_destination)

  def convert(self, *args, **kwargs):
    _path_source = args[0] if len(args) > 0 else kwargs.get('path_source')
    _path_destination = args[0] if len(args) > 0 else kwargs.get('path_destination')

    _format_to = args[1] if len(args) > 1 else kwargs.get('format_to')
    _format_from = args[2] if len(args) > 2 else kwargs.get('format_from')
    _addh = args[3] if len(args) > 3 else kwargs.get('addh', False)

    # Check if to and from formats are valid for OpenBabel
    _obc = OBABEL.OBConversion()
    _obc.SetInAndOutFormats(_format_from, _format_to)

    _mol = OBABEL.OBMol()
    # Open Babel will uncompress .gz files automatically
    _obc.ReadFile(_mol, path_source)

    # Optionally add hydrogens
    if _addh:
      _mol.AddHydrogens()

    _obc.WriteFile(_mol, _path_destination)
