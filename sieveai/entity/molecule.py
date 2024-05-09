from .base import MoleculeBase

class Molecule(MoleculeBase):
  def __init__(self, *args, **kwargs):
    _defaults = {
      "mol_id": None,

      "mol_ext": None,
      "n_models": 0,
      "n_molecules": 0,
      "n_atoms": 0,
      "n_hetatoms": 0,
      "n_residues": 0,

      "db_sources": [],

      "is_valid": None,
      "is_2D": None,
      "is_3D": None,
      "is_gz": None,
      "mol_path": args[0] if len(args) > 0 else kwargs.get('mol_path'),
      "mol_type": args[1] if len(args) > 1 else kwargs.get('mol_type')
    }
    _defaults.update(kwargs)
    super().__init__(*args, **_defaults)

    _mol_path = self.mol_path
    if _mol_path and self.UM.ext(_mol_path) == 'gz':
      self.is_gz = True
      _mol_path = self.UM.filename(_mol_path, with_dir=True)

    self.mol_id = self.UM.filename(_mol_path)
    self.mol_ext = None if _mol_path is None else self.UM.ext(_mol_path)
    self.parse_pdb()

  def parse_pdb(self, *args, **kwargs):
    ...

  # def __str__(self, *args, **kwargs):
  #   return self.mol_id or "Molecule: No Data"

  # def __repr__(self, *args, **kwargs):
  #   return self.mol_id or "Molecule: No Data"

  # File type provider
  def to_format(self, *args, **kwargs):
    _to_ext = args[0] if len(args) > 0 else kwargs.get('to_ext')
    print('to_format', args, self.mol_ext)
