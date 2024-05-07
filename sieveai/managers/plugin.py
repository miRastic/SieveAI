import importlib as ImportLib
from UtilityLib import UtilityManager

class PluginManager(UtilityManager):
  def __init__(self, *args, **kwargs):
    self.plugin_map = {
      'vina': 'Vina',
      'chimerax': 'ChimeraX',
      'hdocklite': 'HDockLite',
      'openbabel': 'OpenBabel',
      'vmdpython': 'VMDPython',
      'annapurna': 'AnnapuRNA',
    }
    super().__init__(**kwargs)

  def get_plugin(self, _plugin_name, _plugin_config:dict = {}):
    # Default Plugin Settings by Package
    # User's choice
    # Runtime config

    _plugin_ref = ImportLib.import_module("..plugins.%s" % _plugin_name, package=__package__)
    _plugin_obj = getattr(_plugin_ref, self.plugin_map.get(_plugin_name) or _plugin_name.title())
    _plugin_ref = _plugin_obj(**_plugin_config)
    return _plugin_ref
