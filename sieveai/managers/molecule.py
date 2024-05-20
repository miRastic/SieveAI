from .base import ManagerBase
from .structure import Structures

class MoleculeManager(ManagerBase):
  mol_type_map = None
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def get_molecules(self, *args, **kwargs):
    """Get molecules with extension as Molecule object

    """
    _path_key = kwargs.get("path_key", args[0] if len(args) > 0 else None)
    _ext = kwargs.get("ext", args[1] if len(args) > 1 else "*.pdb")
    _mol_type = args[2] if len(args) > 2 else kwargs.get("mol_type", "molecule")

    if not _path_key:
      self.settings.messages.error['mol_manager'] = 'No pathkey was passed.'
      return None

    _molecule_paths = self.find_files(self.settings.base[_path_key], _ext)

    _structures_obj = Structures()

    for _mol_path in _molecule_paths:
      _structures_obj.add(_mol_path, _mol_type)

    self.settings.structures.append(_structures_obj)

    return _structures_obj
