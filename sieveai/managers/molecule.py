from .base import ManagerBase
from ..entity import Molecule, Compound, RNA, DNA, Protein

class MoleculeManager(ManagerBase):
  mol_type_map = None
  def __init__(self, *args, **kwargs):
    self.mol_type_map = {
        'molecule': Molecule,
        'compound': Compound,
        'protein': Protein,
        'rna': RNA,
        'dna': DNA,
      }
    super().__init__(**kwargs)

  def get_molecules(self, *args, **kwargs):
    """Get molecules with extension as Molecule object

    """
    _path_key = args[0] if len(args) > 0 else kwargs.get("path_key")
    _ext = args[1] if len(args) > 1 else kwargs.get("ext", "pdb")
    _mol_type = args[2] if len(args) > 2 else kwargs.get("mol_type", 'molecule')

    if not _path_key:
      self.settings.messages.error['mol_manager'] = 'No pathkey was passed.'
      return None

    _molecule_paths = self.find_files(self.settings.base[_path_key], _ext)

    _molecules = []
    if not isinstance(self.settings.molecules[_path_key][_mol_type], (list)):
      self.settings.molecules[_path_key][_mol_type] = []

    for _mol_path in _molecule_paths:
      _mol_obj = self.mol_type_map.get(_mol_type, 'molecule')(_mol_path)
      self.settings.molecules[_path_key][_mol_type].append(_mol_obj)
      _molecules.append(_mol_obj)

    return _molecules
