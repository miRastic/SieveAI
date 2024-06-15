from .molecule import Molecule
from .chain import Chains
from .residue import Residues

class MacroMolecule(Molecule):
  def __init__(self, *args, **kwargs):
    _defaults = {
      "mol_structure": None,
      "macro_category": None,
      "is_macro": True,
      "natural_ligand": None,
      'IUPAC_List': {
        'protein': [
            ("A", "Ala", "Alanine"),
            ("C", "Cys", "Cysteine"),
            ("D", "Asp", "Aspartic Acid"),
            ("E", "Glu", "Glutamic Acid"),
            ("F", "Phe", "Phenylalanine"),
            ("G", "Gly", "Glycine"),
            ("H", "His", "Histidine"),
            ("I", "Ile", "Isoleucine"),
            ("K", "Lys", "Lysine"),
            ("L", "Leu", "Leucine"),
            ("M", "Met", "Methionine"),
            ("N", "Asn", "Asparagine"),
            ("P", "Pro", "Proline"),
            ("Q", "Gln", "Glutamine"),
            ("R", "Arg", "Arginine"),
            ("S", "Ser", "Serine"),
            ("T", "Thr", "Threonine"),
            ("V", "Val", "Valine"),
            ("W", "Trp", "Tryptophan"),
            ("Y", "Tyr", "Tyrosine")
          ],
        'rna': [
            ("A", "Adenine"),
            ("C", "Cytosine"),
            ("G", "Guanine"),
            ("U", "Uracil"),
            ("R", "A or G"),
            ("Y", "C or T"),
            ("S", "G or C"),
            ("W", "A or T"),
            ("K", "G or T"),
            ("M", "A or C"),
            ("B", "C or G or T"),
            ("D", "A or G or T"),
            ("H", "A or C or T"),
            ("V", "A or C or G"),
            ("N", "any base"),
            (".", "gap"),
            ("-", "gap"),
         ],
        'dna': [
              ("A", "Adenine"),
              ("C", "Cytosine"),
              ("G", "Guanine"),
              ("T", "Thymine"),
              ("R", "A or G"),
              ("Y", "C or T"),
              ("S", "G or C"),
              ("W", "A or T"),
              ("K", "G or T"),
              ("M", "A or C"),
              ("B", "C or G or T"),
              ("D", "A or G or T"),
              ("H", "A or C or T"),
              ("V", "A or C or G"),
              ("N", "any base"),
              (".", "gap"),
              ("-", "gap"),
            ]
      }
    }
    _defaults.update(kwargs)
    super().__init__(*args, **_defaults)

  # _1L_codes = None
  # @property
  # def IUPAC_codes(self):
  #   if self._1L_codes is None:
  #     self._1L_codes = [_l[0] for _l in self.IUPAC]
  #   return self._1L_codes

  # _residue_names = None
  # @property
  # def IUPAC_names(self):
  #   if self._residue_names is None:
  #     self._residue_names = [_l[-1] for _l in self.IUPAC]
  #   return self._residue_names

  # _3L_codes = None
  # @property
  # def IUPAC_3L_codes(self):
  #   "Implemnted in respective molecules"
  #   return self._3L_codes

class Protein(MacroMolecule):
  def __init__(self, *args, **kwargs):
    _defaults = {
      "mol_cat": 'protein',
    }
    _defaults.update(kwargs)
    super().__init__(*args, **_defaults)
    self.IUPAC = self.IUPAC_List.protein
    self.is_protein = True

  _residue_3L_codes = None
  @property
  def IUPAC_3L_codes(self):
    if self._residue_3L_codes is None:
      self._residue_3L_codes = [_l[1] for _l in self.IUPAC]
    return self._residue_3L_codes

class DNA(MacroMolecule):
  def __init__(self, *args, **kwargs):
    _defaults = {
      "mol_cat": 'dna',
    }
    _defaults.update(kwargs)
    super().__init__(*args, **_defaults)
    self.IUPAC = self.IUPAC_List.dna
    self.is_dna = True

class RNA(MacroMolecule):
  def __init__(self, *args, **kwargs):
    _defaults = {
      "mol_cat": 'rna',
    }
    _defaults.update(kwargs)
    super().__init__(*args, **_defaults)
    # self.IUPAC = self.IUPAC_List.rna
    # self.is_rna = True
