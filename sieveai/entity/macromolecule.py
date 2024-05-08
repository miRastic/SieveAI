from UtilityLib import UM
from .molecule import Molecule

class MacroMolecule(Molecule):
  def __init__(self, *args, **kwargs):
    self.mol_structure = None
    self.n_chains = 0
    self.natural_ligand = None
    self.parse_pdb()
    super().__init__(**kwargs)

  def parse_pdb(self, *args, **kwargs):
    return None
    if not self.mol_structure is None:
      return
    _biopython = [UM.require('Bio', 'BioPy'), UM.require('Bio.PDB', 'BioPDB')]
    if all(_biopython) and self.mol_ext == 'pdb':
      try:
        _parser = UM.BioPDB.PDBParser(QUIET=True)
        self.mol_pdb = _parser.get_structure(self.mol_id, self.mol_path)
        # List models/molecules, chains, residues, atoms
      except Exception as _e:
        self.mol_error = f'Error in accessing molecule {self.mol_id}: {_e}'
    else:
      ...

class Protein(MacroMolecule):
  def __init__(self, *args, **kwargs):
    self.mol_type = 'protein'
    super().__init__(**kwargs)

class DNA(MacroMolecule):
  def __init__(self, *args, **kwargs):
    self.mol_type = 'dna'
    super().__init__(**kwargs)

class RNA(MacroMolecule):
  def __init__(self, *args, **kwargs):
    self.mol_type = 'rna'
    super().__init__(**kwargs)
