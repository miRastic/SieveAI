from .molecule import Molecule

class MacroMolecule(Molecule):
  def __init__(self, *args, **kwargs):
    _defaults = {
      "mol_structure": None,
      "n_chains": 0,
      "natural_ligand": None,
    }
    _defaults.update(kwargs)
    super().__init__(*args, **_defaults)
    self.parse_pdb()

  def parse_pdb(self, *args, **kwargs):
    return None
    if not self.mol_structure is None:
      return
    _biopython = [self.UM.require('Bio', 'BioPy'), self.UM.require('Bio.PDB', 'BioPDB')]
    if all(_biopython) and self.mol_ext == 'pdb':
      try:
        _parser = self.UM.BioPDB.PDBParser(QUIET=True)
        self.mol_pdb = _parser.get_structure(self.mol_id, self.mol_path)
        # List models/molecules, chains, residues, atoms
      except Exception as _e:
        self.mol_error = f'Error in accessing molecule {self.mol_id}: {_e}'
    else:
      ...

class Protein(MacroMolecule):
  def __init__(self, *args, **kwargs):
    _defaults = {
      "mol_type": 'protein'
    }
    _defaults.update(kwargs)
    super().__init__(*args, **_defaults)

class DNA(MacroMolecule):
  def __init__(self, *args, **kwargs):
    _defaults = {
      "mol_type": 'dna'
    }
    _defaults.update(kwargs)
    super().__init__(*args, **_defaults)

class RNA(MacroMolecule):
  def __init__(self, *args, **kwargs):
    _defaults = {
      "mol_type": 'rna'
    }
    _defaults.update(kwargs)
    super().__init__(*args, **_defaults)
