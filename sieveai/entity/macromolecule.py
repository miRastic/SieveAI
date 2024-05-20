from .molecule import Molecule
from .chain import Chains
from .residue import Residues

class MacroMolecule(Molecule):
  def __init__(self, *args, **kwargs):
    _defaults = {
      "mol_structure": None,
      "n_chains": None, # Total Number of chains
      "_chains": Chains(), # List of Chains
      "n_residues": None, # Total Number of Residues
      "_residues": Residues(), # List of Residues with Chain identifier
      "natural_ligand": None,
    }
    _defaults.update(kwargs)
    self.update(_defaults)

class Protein(MacroMolecule):
  def __init__(self, *args, **kwargs):
    _defaults = {
      "mol_cat": 'protein'
    }
    _defaults.update(kwargs)
    self.update(_defaults)

class DNA(MacroMolecule):
  def __init__(self, *args, **kwargs):
    _defaults = {
      "mol_cat": 'dna'
    }
    _defaults.update(kwargs)
    self.update(_defaults)

class RNA(MacroMolecule):
  def __init__(self, *args, **kwargs):
    _defaults = {
      "mol_cat": 'rna'
    }
    _defaults.update(kwargs)
    self.update(_defaults)
