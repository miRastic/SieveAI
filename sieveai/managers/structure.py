from UtilityLib import PM, ObjDict
from ..entity import Molecule, Compound, RNA, DNA, Protein
from .plugin import PluginManager as Plugins

class Structure(ObjDict):
  molecule = None
  def __init__(self, *args, **kwargs):
    _mol_id = kwargs.get("mol_path", args[0] if len(args) > 0 else 'Unknown-XXX')
    _mol_path = kwargs.get("mol_path", args[1] if len(args) > 1 else None)
    _mol_parser = kwargs.get("mol_parser", args[2] if len(args) > 2 else Molecule)

    _defaults = {
      "mol_id": _mol_id,
      "mol_ext": None,

      "mol_file_size": None, # bytes

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
      "mol_type": None,
      "mol_format": None,
      "mol_path": _mol_path,
      "mol_parser": _mol_parser,
      "molecule": _mol_parser(_mol_path)
    }

    _defaults.update(kwargs)
    self.update(_defaults)
    self.parse_additional_attributes()

  def parse_additional_attributes(self):
    _mol_path = self.mol_path
    if _mol_path and PM.ext(_mol_path) == 'gz':
      self.is_gz = True
      _mol_path = PM.filename(_mol_path, with_dir=True)

    self.mol_id = PM.filename(_mol_path)
    self.mol_ext = None if _mol_path is None else PM.ext(_mol_path)
    _, self.mol_file_size, _f_unit = PM.get_file_size(_mol_path)

  def to_format(self, *args, **kwargs):
    _to = kwargs.get('to', args[0] if len(args) > 0 else None)
    if _to is None:
      return

    print('Self.Molecule', self.mol_path, self)
    _xyz = Plugins.share_plugin('openbabel')
    _res = _xyz.convert(
      self.mol_path, PM.change_ext(self.mol_path, _to),
      format_to=_to, format_from=self.mol_ext)
    print('res', _res)

class Structures(ObjDict):
  molecules = {}
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
      'compound': Compound,
      'protein': Protein,
      'rna': RNA,
      'dna': DNA,
    }

  def __init__(self, *args, **kwargs):
    ...

  def add(self, *args, **kwargs):
    _mol_path = kwargs.get("mol_path", args[0] if len(args) > 0 else None)
    _mol_type = kwargs.get("mol_type", args[1] if len(args) > 1 else "molecule")

    _mol_id = PM.filename(_mol_path)
    _mol_parser = self.mol_type_map.get(_mol_type, 'molecule')

    _mol_obj = Structure(**{
        'mol_ext': PM.file_ext(_mol_path),
        'mol_format': PM.file_ext(_mol_path), # Determine the mol_format
        'mol_id': _mol_id,
        'mol_parser': _mol_parser,
        'mol_type': _mol_type,
        'mol_path': _mol_path,
      })

    self.molecules[_mol_obj.mol_id] = _mol_obj

  def __getitem__(self, *args, **kwargs):
    _key = args[0] if len(args) > 0 else kwargs.get('key', self.molecules.keys()[0])
    return self.molecules[_key]

  def __iter__(self, *args, **kwargs):
    for _mol_id, _mol_obj in self.molecules.items():
      yield (_mol_id, _mol_obj)

  def __len__(self):
    return len(self.molecules.keys())

  def parse_pdb(self, *args, **kwargs):
    return None
    if not self.mol_structure is None:
      return
    _biopython = [PM.require('Bio', 'BioPy'), PM.require('Bio.PDB', 'BioPDB')]
    if all(_biopython) and self.mol_ext == 'pdb':
      try:
        _parser = PM.BioPDB.PDBParser(QUIET=True)
        self.mol_pdb = _parser.get_structure(self.mol_id, self.mol_path)
        # List models/molecules, chains, residues, atoms
      except Exception as _e:
        self.mol_error = f'Error in accessing molecule {self.mol_id}: {_e}'
    else:
      ...
