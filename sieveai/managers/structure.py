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
    self.ext_molecules = kwargs.get('ext_molecules', args[1] if len(args) > 1 else ".pdb")
    self.type_molecules = kwargs.get('type_molecules', args[2] if len(args) > 2 else None)
    self.molecules = {}
    self._discover_molecules()

  def _discover_molecules(self):
    if self.path_molecules.exists():
      _ext = self.ext_molecules
      if not '*' in _ext:
        _ext = f"*{_ext}"
      for _file in self.path_molecules.search(_ext):
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

  def generic_converter(self, *args, **kwargs):
    path_source = kwargs.get('path_source', args[0] if len(args) > 0 else None)
    path_target = kwargs.get('path_target', args[1] if len(args) > 1 else None)
    ext_source = kwargs.get('ext_source', args[2] if len(args) > 2 else None)
    ext_target = kwargs.get('ext_target', args[3] if len(args) > 3 else None)

    print(path_source, ext_source, path_target, ext_target)
    return path_target

  def set_format(self, ext='pdbqt', mol_id=None, converter=None, **kwargs) -> None:
    ext = str(ext).strip('.')
    _conversion_method_maps = {
      'pdbqt': self.generic_converter,
    }

    _method = converter if not converter is None else _conversion_method_maps.get(ext, self.generic_converter)

    if not callable(_method):
      return False

    _items = []
    if mol_id:
      _items.append((mol_id,  self[mol_id]))
    else:
      _items =  self.items

    for _mol_id, _mol_obj in _items:
      _target_path = _mol_obj.mol_path.with_suffix(f".{ext}")
      _target_path.parents[0].validate()
      self[_mol_id][f"mol_path_{ext}"] = _method(_mol_obj.mol_path, _target_path,
                                             _mol_obj.mol_ext.strip('.'), ext, **kwargs)


    return True

  @property
  def items(self):
    return list(self.molecules.items())

  def keys(self):
    return list(self.molecules.keys())

  @property
  def ids(self):
    return self.keys()

  mol_ids = ids
