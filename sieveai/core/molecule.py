class MoleculeBase():
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

class Molecule(MoleculeBase):
  mol_id = None
  mol_path = None
  mol_type = None
  n_models = 0
  n_molecules = 0
  n_atoms = 0
  n_hetatoms = 0
  n_residues = 0

  db_sources = []

  is_valid = False
  is_2D = False
  is_3D = False

  available_extensions = None

  original_extension = None

  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def __str__(self, *args, **kwargs):
    return self.mol_id or "Molecule: No Data"

  def __repr__(self, *args, **kwargs):
    return self.mol_id or "Molecule: No Data"

  # File type provider
  def to_extension(self, *args, **kwargs):
    print("Not yet implemented")
    ...

class Compound(Molecule):
  mol_type = 'compound'
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

class Protein(Molecule):
  mol_type = 'protein'
  natural_ligand = None
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

class DNA(Molecule):
  mol_type = 'dna'
  natural_ligand = None
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

class RNA(Molecule):
  mol_type = 'rna'
  natural_ligand = None
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
