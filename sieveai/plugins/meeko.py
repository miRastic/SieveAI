
from .base import PluginBase

from meeko import MoleculePreparation, PDBQTWriterLegacy
from rdkit import Chem

class Meeko(PluginBase):
  is_ready = False
  plugin_name = "Meeko"
  process = ['conversion']
  url = "https://github.com/forlilab/Meeko"

  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def setup(self, *args, **kwargs):
    self.update_attributes(self, kwargs)

  def convert(self, *args, **kwargs):
    _path_source = kwargs.get('path_source', args[0] if len(args) > 0 else None)
    _path_destination = kwargs.get('path_destination', args[1] if len(args) > 1 else None)

    _format_to = kwargs.get('format_to', args[2] if len(args) > 2 else None)
    _format_from = kwargs.get('format_from', args[3] if len(args) > 3 else None)
    _addH = kwargs.get('addH', args[4] if len(args) > 4 else True)
    _removeH = kwargs.get('removeH', args[4] if len(args) > 4 else True)

    _molecules = Chem.SDMolSupplier(_path_source, removeHs=False) if _format_from is 'sdf' else [Chem.MolFromPDBFile(_path_source)]

    # there is one molecule in this SD file, this loop iterates just once
    for _mol in _molecules:
      _preparator = MoleculePreparation()
      _mol_setups = _preparator.prepare(_mol)
      for _setup in _mol_setups:
        # _setup.show() # optional
        _pdbqt_string, _, _ = PDBQTWriterLegacy.write_string(_setup)
        self.write(_path_destination, _pdbqt_string)
