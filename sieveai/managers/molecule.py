from .base import ManagerBase
from ..core.molecule import Molecule, Compound, RNA, DNA, Protein

class MoleculeManager(ManagerBase):
  mol_type_map = {
      'molecule': Molecule,
      'protein': Protein,
      'compound': Compound,
      'rna': RNA,
      'dna': DNA,
    }
  def __init__(self, *args, **kwargs):
    # self.mol_type_map =
    super().__init__(**kwargs)

  def get_molecules(self, *args, **kwargs):
    """Get molecules with extension as Molecule object

    """
    _path_key = args[0] if len(args) > 0 else kwargs.get("path_key", "pdb")
    _ext = args[1] if len(args) > 1 else kwargs.get("ext", )
    _mol_type = args[1] if len(args) > 1 else kwargs.get("mol_type", 'molecule')

    _molecules = self.find_files(self.settings.base[_path_key], _ext)
    _all_molecules = []

    for _mol_path in _molecules:
      print(_mol_type, self.mol_type_map.get(_mol_type, 'molecule'))
      _all_molecules.append(self.mol_type_map.get(_mol_type, 'molecule')(_mol_path))

    return _all_molecules
