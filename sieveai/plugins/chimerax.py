
from .base import PluginBase
from ..plug import EntityPath

class ChimeraX(PluginBase):
  is_ready = False
  plugin_name = "ChimeraX"
  process = ['analysis', 'conversion']
  url = "https://www.cgl.ucsf.edu/chimerax/docs/user/index.html"

  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
    self.require('requests', 'REQUESTS')
    self.require('json', 'JSON')
    self.require('pandas', 'PD')
    self.require('re', 'RegEx')
    self.re_contacts = self.RegEx.compile(f"(\d+) contacts")
    self.re_hbonds = self.RegEx.compile(f"(\d+) H-bonds")

  def setup(self, *args, **kwargs):
    self.update_attributes(self, kwargs)

  def boot(self, *args, **kwargs):
    ...

  def run(self, *args, **kwargs):
    ...

  def shutdown(self, *args, **kwargs):
    ...

  def start_remote(self, *args, **kwargs) -> None:
    _start_chimerax = "chimerax --cmd 'remotecontrol rest start port 45385 json 1' &"
    self.OS.system(_start_chimerax)

  def request(self, *args, **kwargs):
    """
    Example: .request(params={"command": "surface #1; measure volume #1;"})

    """
    _url = kwargs.get("url", args[0] if len(args) > 0 else "http://127.0.0.1:45385/run")
    _params = kwargs.get("params", args[1] if len(args) > 1 else {})
    _return_type = kwargs.get("return_type", args[2] if len(args) > 2 else "json")
    _method = kwargs.get("method", args[3] if len(args) > 3 else 'get')

    if not _url:
      return None

    if _method == 'post':
      _r = self.REQUESTS.post(url=_url, data=self.JSON.dumps(_params))
    else:
      _r = self.REQUESTS.get(url=_url, params=_params)

    # Return other requests
    if _r.status_code == 200 and _return_type == 'json':
      _r = _r.json()

    return _r

  def exe_cxc_file(self, file_path=None):
    if file_path is None:
      return

    _res = self.cmd_run(*["chimerax",
      "--cmd", f"open {file_path}",
      "--silent",
      "--offscreen",
    ])
    return _res

  def _parse_hbond_line(self, line):
    _result = None
    if "#" in line:
      pass
    elif "/" in line:
      # Since Model ID is 1 and only Chain ID is given so appending to keep the syntax intact
      line = str(line).replace("/", "Structure #1/")
    else:
      raise Exception("Unknown type of col separators.")

    cols = line.split("#")

    if len(cols):
      try:
        # Use Second Column to get Donor
        donor = tuple(cols[1].split()[:4])
        # Use Third Column to get acceptor
        acceptor = tuple(cols[2].split()[:4])
        # Use fourth colun to get Hydrogen and HBond length
        hydrogen = tuple(cols[3].split()[:4])
        length = tuple(cols[3].split()[-2:])
        _result = {
          "donor": donor,
          "acceptor": acceptor,
          "hydrogen": hydrogen,
          "length": length
        }
      except:
        length = None

    return _result

  def _parse_hbonds_file(self, file_path):
    _hb_attribs = []
    file_path = EntityPath(file_path)
    if file_path.exists():
      _res_line_flag = False
      key_term = 'H-bonds'
      for line in file_path.readlines():
        line = line.strip()
        # print(_res_line_flag, search_regex.search(line))
        if _res_line_flag and not line.startswith(key_term) and "#" in line:
          _res = self._parse_hbond_line(line)
          if _res:
            _hb_attribs.append(_res)
        if not _res_line_flag and self.re_hbonds.search(line):
          _res_line_flag = True
          if not int(self.re_hbonds.search(line).group(1)) > 0:
            return _hb_attribs

    return _hb_attribs

  def _parse_contacts_line(self, line):
    _result = None
    if "#" in line:
      pass
    elif "/" in line:
      # Since Model ID is 1 and only Chain ID is given so appending to keep the syntax intact
      line = str(line).replace("/", "Structure #1/")
    else:
      self.log_error("ChimeraX: Unknown type of col separators.")

    _cols = line.split("#")
    # print(cols); self.log_error("Unknown type of col separators.")

    if len(_cols):
      # Use Second Column to get Atom1
      _atom1 = tuple(_cols[1].split()[:4])
      # Use Third Column to get Atom2
      _atom2 = tuple(_cols[2].split()[:4])
      # Use fourth colun to get Hydrogen and HBond length
      _overlap = _cols[2].split()[-2]
      _distance = _cols[2].split()[-1]
      _result = {
        "atom1": _atom1,
        "atom2": _atom2,
        "overlap": _overlap,
        "distance": _distance
      }

    return _result

  def _parse_contacts_file(self, file_path):
    file_path = EntityPath(file_path)

    _contact_attrib = []
    if file_path.exists():
      _res_line_flag = False

      for line in file_path.readlines():
        line = line.strip()
        if _res_line_flag and not len({"atom1", "atom2"} & set(line.split())):
          _res = self._parse_contacts_line(line)
          if _res:
            _contact_attrib.append(_res)
        if not _res_line_flag and self.re_contacts.search(line):
          _res_line_flag = True
          if not int(self.re_contacts.search(line).group(1)) > 0:
            return _contact_attrib

    return _contact_attrib

  def _parse_atom_identity(self, atom_details: tuple = ()):
    if atom_details and type(atom_details) is tuple and len(atom_details) == 4:
      atom_details_model = atom_details[0].split("/")[0]
      atom_details_chain = atom_details[0].split("/")[1]
      atom_details_resname = atom_details[1]
      atom_details_resid = atom_details[2]
      atom_details_atom = atom_details[3]

      model_id = atom_details_model
      sub_model_id = None
      if "." in atom_details_model:
        model_id = atom_details_model.split(".")[0]
        sub_model_id = atom_details_model.split(".")[1]

      __result = {
        "model_id": model_id,
        "sub_model_id": sub_model_id,
        "chain": atom_details_chain,
        "resname": atom_details_resname,
        "resid": atom_details_resid,
        "atom": atom_details_atom,
      }

      return __result
    else:
      raise Exception(f"Problem in atom records {atom_details}")

  def parse_contacts(self, file_path):
    _contacts = self.DF(self._parse_contacts_file(file_path))

    if not _contacts.shape[0]:
        return None

    _contacts["atom1"] = _contacts["atom1"].apply(self._parse_atom_identity)
    _contacts["atom2"] = _contacts["atom2"].apply(self._parse_atom_identity)

    _contacts = self.PD.concat([_contacts.drop(['atom1'], axis=1), _contacts['atom1'].apply(self.PD.Series)], axis=1)
    _contacts.rename(columns={'model_id': 'atom1__model_id', 'sub_model_id': 'atom1__sub_model_id', 'chain': 'atom1__chain', 'resname': 'atom1__resname', 'resid': 'atom1__resid', 'atom': 'atom1__atom'}, inplace=True)

    _contacts = self.PD.concat([_contacts.drop(['atom2'], axis=1), _contacts['atom2'].apply(self.PD.Series)], axis=1)
    _contacts.rename(columns={'model_id': 'atom2__model_id', 'sub_model_id': 'atom2__sub_model_id', 'chain': 'atom2__chain', 'resname': 'atom2__resname', 'resid': 'atom2__resid', 'atom': 'atom2__atom'}, inplace=True)

    return _contacts

  def parse_hbonds(self, file_path):
    _hbonds = self.DF(self._parse_hbonds_file(file_path))

    if not _hbonds.shape[0]:
      return None

    _hbonds["donor"] = _hbonds["donor"].apply(self._parse_atom_identity)
    _hbonds["acceptor"] = _hbonds["acceptor"].apply(self._parse_atom_identity)
    _hbonds["hydrogen"] = _hbonds["hydrogen"].apply(self._parse_atom_identity)

    _hbonds = self.PD.concat([_hbonds.drop(['donor'], axis=1), _hbonds['donor'].apply(self.PD.Series)], axis=1)
    _hbonds.rename(columns={'model_id': 'donor__model_id', 'sub_model_id': 'donor__sub_model_id', 'chain': 'donor__chain', 'resname': 'donor__resname', 'resid': 'donor__resid', 'atom': 'donor__atom'}, inplace=True)

    _hbonds = self.PD.concat([_hbonds.drop(['acceptor'], axis=1), _hbonds['acceptor'].apply(self.PD.Series)], axis=1)
    _hbonds.rename(columns={'model_id': 'acceptor__model_id', 'sub_model_id': 'acceptor__sub_model_id', 'chain': 'acceptor__chain', 'resname': 'acceptor__resname', 'resid': 'acceptor__resid', 'atom': 'acceptor__atom'}, inplace=True)

    _hbonds = self.PD.concat([_hbonds.drop(['hydrogen'], axis=1), _hbonds['hydrogen'].apply(self.PD.Series)], axis=1)
    _hbonds.rename(columns={'model_id': 'hydrogen__model_id', 'sub_model_id': 'hydrogen__sub_model_id', 'chain': 'hydrogen__chain', 'resname': 'hydrogen__resname', 'resid': 'hydrogen__resid', 'atom': 'hydrogen__atom'}, inplace=True)

    return _hbonds
