from ..entity import Molecule, Compound, MacroMolecule, RNA, DNA, Protein

class Structures():
  mol_formats = {
    'pdb': 'PDB',
    'pdbqt': 'PDBQT',
    'sdf': 'SDF',
    'mol2': 'MOL2',
    'mol': 'MOL',
    'lig': 'LIG',
  }
  mol_type_map = {
      'molecule': Molecule,
      'macromolecule': MacroMolecule,
      'compound': Compound,
      'protein': Protein,
      'rna': RNA,
      'dna': DNA,
    }

  def __init__(self, *args, **kwargs):
    self.path_molecules = kwargs.get('path_molecules', args[0] if len(args) > 0 else None)
    self.ext_molecules = kwargs.get('ext_molecules', args[1] if len(args) > 1 else None)
    self.type_molecules = kwargs.get('type_molecules', args[2] if len(args) > 2 else None)
    self.molecules = {}
    self._discover_molecules()

  def _discover_molecules(self):
    if self.path_molecules.exists():
      for _file in self.path_molecules.files():
        # Get unique ID instead of stem
        self.molecules[_file.stem] = self.mol_type_map.get(self.type_molecules)(_file.stem, _file)

  def __repr__(self, *args, **kwargs):
    return f"""Structures of type: {self.type_molecules} with extension {self.ext_molecules} from {self.path_molecules}."""

  def __getitem__(self, *args, **kwargs):
    try:
      _first_key = self.molecules.keys()[0]
    except:
      _first_key = None

    _key = kwargs.get('key', args[0] if len(args) > 0 else _first_key)
    return self.molecules.get(_key)

  def __iter__(self, *args, **kwargs):
    for _mol_id, _mol_obj in self.molecules.items():
      yield (_mol_id, _mol_obj)

  def __len__(self):
    return len(self.molecules.keys())

  len = __len__

  def items(self):
    return list(self.molecules.items())

  def keys(self):
    return list(self.molecules.keys())

  ids = keys
  mol_ids = keys

  def parse_pdb(self, *args, **kwargs):
    return None
    if not self.mol_structure is None:
      return
    # _biopython = [SieveAIBaseInit.require('Bio', 'BioPy'), SieveAIBaseInit.require('Bio.PDB', 'BioPDB')]
    # if all(_biopython) and self.mol_ext == 'pdb':
    #   try:
    #     _parser = SieveAIBaseInit.BioPDB.PDBParser(QUIET=True)
    #     self.mol_pdb = _parser.get_structure(self.mol_id, self.mol_path)
    #     # List models/molecules, chains, residues, atoms
    #   except Exception as _e:
    #     self.mol_error = f'Error in accessing molecule {self.mol_id}: {_e}'
    # else:
    #   ...
