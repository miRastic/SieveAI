from UtilityLib import ObjDict
from .base import ManagerBase

class ConfigManager(ManagerBase):
  settings = ObjDict()
  def __init__(self, *args, **kwargs):
    self.__set_defaults()
    super().__init__(**kwargs)
  
  def __set_defaults(self):
    _common_vars = {
      'path_project': None,

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
    _executables.plugins.docking = []
    _executables.plugins.rescoring = []
    _executables.programs.docking = ['vina']
    _executables.programs.rescoring = []

    self.settings.base.update(_common_vars)
    self.settings.exe.update(_executables)

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

