from .base import MoleculeBase

class Molecule(MoleculeBase):
  def __init__(self, *args, **kwargs):
    _mol_id = kwargs.get("mol_id", args[0] if len(args) > 0 else 'Unknown-XXX')
    _mol_path = kwargs.get("mol_path", args[1] if len(args) > 1 else None)

    _defaults = {
      "mol_id": _mol_id,
      "mol_path": _mol_path,
    }
    _defaults.update(kwargs)
    super().__init__(*args, **_defaults)
    self.parse_additional_attributes()

  def parse_additional_attributes(self) -> None:
    _other_attribs = {
      "mol_ext": self.mol_path.ext(),
      "mol_file_size": self.mol_path.size,

      # "n_models": 0,
      # "n_molecules": 0,
      # "n_hetatoms": 0,
      # "n_residues": 0,

      # "db_sources": [],

      "is_valid": None,
      "is_2D": None,
      "is_3D": None,
      "is_gz": None,
      "mol_type": None,
      "mol_format": None,
      "mol_hash": self.mol_path.hash,
    }

    _mol_path = self.mol_path

    if '.gz' in _mol_path.suffixes:
      _mol_path = _mol_path.with_suffix('') # Remove last suffix

    self.update(_other_attribs)
