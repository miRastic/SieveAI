from UtilityLib import ObjDict, UM
from .base import MoleculeBase

class Molecule(MoleculeBase):
  def __init__(self, *args, **kwargs):
    self.mol_id = None

    self.mol_ext = None
    self.n_models = 0
    self.n_molecules = 0
    self.n_atoms = 0
    self.n_hetatoms = 0
    self.n_residues = 0

    self.db_sources = []

    self.is_valid = False
    self.is_2D = False
    self.is_3D = False
    self.is_gz = False

    self.mol_path = args[0] if len(args) > 0 else kwargs.get('mol_path')
    self.mol_type = args[1] if len(args) > 1 else kwargs.get('mol_type')

    _mol_path = self.mol_path
    if _mol_path and UM.ext(_mol_path) == 'gz':
      self.is_gz = True
      _mol_path = UM.filename(_mol_path, with_dir=True)
    
    self.mol_id = UM.filename(_mol_path)
    self.mol_ext = None if _mol_path is None else UM.ext(_mol_path)
    super().__init__(**kwargs)
    self.parse_pdb()

  def parse_pdb(self, *args, **kwargs):
    ...

  def __str__(self, *args, **kwargs):
    return self.mol_id or "Molecule: No Data"

  def __repr__(self, *args, **kwargs):
    return self.mol_id or "Molecule: No Data"

  # File type provider
  def to_format(self, *args, **kwargs):
    print("Not yet implemented")
    ...
