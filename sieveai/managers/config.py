from UtilityLib import ObjDict
from .base import ManagerBase

class ConfigManager(ManagerBase):
  settings = ObjDict()
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
    self.__set_defaults()
    self.__process_config()

  def __process_config(self):
    if self.settings.base.path_receptors is None:
      self.settings.base.path_receptors = self.get_path(self.settings.base.dir_receptors)

    if self.settings.base.path_ligands is None:
      self.settings.base.path_ligands = self.get_path(self.settings.base.dir_ligands)

    if self.settings.base.path_docking is None:
      self.settings.base.path_docking = self.get_path(self.settings.base.dir_docking)

    if self.settings.base.path_analysis is None:
      self.settings.base.path_analysis = self.get_path(self.settings.base.dir_analysis)

    if self.settings.base.path_results is None:
      self.settings.base.path_results = self.get_path(self.settings.base.dir_results)

  def __set_defaults(self):
    _common_vars = {
      'path_base': None,

      'path_receptors': None,
      'path_ligands': None,
      'path_docking': None,
      'path_analysis': None,
      'path_results': None,
      'path_plots': None,

      'dir_receptors': 'receptors',
      'dir_ligands': 'ligands',
      'dir_docking': 'docking',
      'dir_analysis': 'analysis',
      'dir_results': 'results',
      'dir_plots': 'plots',
    }

    _executables = ObjDict()
    _executables.plugins.docking = ObjDict()
    _executables.plugins.rescoring = ObjDict()
    _executables.programs.docking = ['vina']
    _executables.programs.rescoring = []

    self.settings.base.update(_common_vars)
    self.settings.exe.update(_executables)
    self.settings.plugin_data = ObjDict()
    self.settings.molecules = ObjDict()
    self.settings.messages = ObjDict()
    self.settings.messages.error = ObjDict()
    self.settings.messages.info = ObjDict()
    self.settings.messages.warning = ObjDict()

  def _read_config(self, *args, **kwargs):
    _config_path = ""
    if (self.exists(_config_path)):
      # Read config file
      ...
    else:
      # Write a default config file
      ...

  def _write_config(self, *args, **kwargs):

    ...
