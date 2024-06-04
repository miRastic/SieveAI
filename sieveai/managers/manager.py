from .config import ConfigManager
from .plugin import PluginManager

class Manager(ConfigManager):
  ref_processes = None

  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  # Manage commandline operations
  def _update_cli_args(self):
    # key: (['arg_k1', 'arg_k2'], nargs, default, help, {})
    _version_info = f"TEST (build-TEST)"
    _cli_settings = {
      "debug": (['--debug'], None, 0, 'silent/verbose/debug mode from 0, 1, 2, and 3.', {}),
      "path_base": (['-b'], "*", [self.OS.getcwd()], 'Provide base directory to run the process.', {}),
      "dir_receptors": (['-r'], None, 'receptors', 'Directory name containing receptors.', {}),
      "dir_ligands": (['-l'], None, 'ligands', 'Directory name containing ligands.', {}),
      "docking_programs": (['-d'], "*", ['vina'], 'One or more Docking Programs eg: vina, hdocklite, auto.', {}),
    }

    _params = self.get_cli_args(_cli_settings, version=_version_info)

    print("{}\n{}\n{}".format("=" * len(_version_info), _version_info, "=" * len(_version_info)))
    self.settings.base.update(_params)

  def get_settings(self, obj_key=None, sep='.'):
    if isinstance(obj_key, (str)):
      return self.get_deep_key(self.settings, obj_key, sep=sep)
    else:
      return self.settings

  def get_plugin(self, _plugin_name):
    return PluginManager.share_plugin(_plugin_name)

  def _manage_exe_plugins(self, *args, **kwargs):
    _plugin_type = kwargs.get("plugin_type", args[0] if len(args) > 0 else "docking")

    if not isinstance(self.settings.exe.plugin_refs[_plugin_type], (dict)):
      self.settings.exe.plugin_refs[_plugin_type] = {}

    for _dp in self.settings.exe.plugin_list[_plugin_type] or []:
      self.settings.exe.plugin_refs[_plugin_type][_dp] = self.get_plugin(_dp)

  def handle_docking(self, *args, **kwargs):
    from ..process.process import Process
    self.settings.base.update(kwargs)

    if self.settings.base.path_base:
      self.path_base = self.settings.base.path_base

    self.log_debug(f'Current base path is {self.path_base}')

    if self.settings.base.docking_programs and len(self.settings.base.docking_programs) > 0:
      self.settings.exe.plugin_list.docking = self.settings.base.docking_programs

    self._manage_exe_plugins('docking')
    self._manage_exe_plugins('analysis')

    self.ref_processes = Process(path_base=self.path_base, settings=self.settings) # pass settings to Dock
    self.log_debug(f'Starting docking with plugins {tuple(self.settings.exe.plugin_list.docking)}.')
    self.ref_processes.process()

  def get_process_status(self, *args, **kwargs):
    _status = {
      "queue": self.queue_task_status()
    }
    for _idx, _item in self.settings.plugin_data.items():
      _status[_idx] = _item.status()

    return _status

  def cli_dock(self):
    self._update_cli_args()
    self.handle_docking()

  # Manage web operation

  def _update_web_args(self):
    ...

  def web_dock(self):
    self._update_web_args()
    self.handle_docking()

  def web_server(self, *args, **kwargs):
    from .web import SieveAIAPI
    _wm = SieveAIAPI(*args, **kwargs)
    _wm.run_server()
    return _wm
