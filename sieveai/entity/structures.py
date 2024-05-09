from . import Molecule, Compound, RNA, DNA, Protein

class Structures():
  molecules = {}
  mol_type_map = {
      'molecule': Molecule,
      'compound': Compound,
      'protein': Protein,
      'rna': RNA,
      'dna': DNA,
    }
  def __init__(self, *args, **kwargs):
    ...

  def add(self, *args, **kwargs):
    _mol_path = args[0] if len(args) > 0 else kwargs.get("mol_path", "molecule")
    _mol_type = args[1] if len(args) > 1 else kwargs.get("mol_type", "molecule")
    _mol_obj = self.mol_type_map.get(_mol_type, 'molecule')(_mol_path)
    self.molecules[_mol_obj.mol_id] = _mol_obj

  def __getitem__(self, *args, **kwargs):
    _key = args[0] if len(args) > 0 else kwargs.get('key', self.molecules.keys()[0])
    return self.molecules[_key]

  def __iter__(self, *args, **kwargs):
    for _mol_id, _mol_obj in self.molecules.items():
      yield (_mol_id, _mol_obj)

  def __len__(self):
    return len(self.molecules.keys())
