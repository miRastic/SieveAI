import importlib as ImportLib
from UtilityLib import UtilityManager

class PluginManager(UtilityManager):
  plugin_map = {
    'vina': 'Vina',
    'chimerax': 'ChimeraX',
    'hdocklite': 'HDockLite',
    'openbabel': 'OpenBabel',
    'vmdpython': 'VMDPython',
    'annapurna': 'AnnapuRNA',
    'meeko': 'Meeko',
  }
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  @staticmethod
  def share_plugin(_plugin_name):
    _plugin_ref = ImportLib.import_module("..plugins.%s" % _plugin_name, package=__package__)
    _plugin_obj = getattr(_plugin_ref, PluginManager.plugin_map.get(_plugin_name) or _plugin_name.title())
    return _plugin_obj


  def get_plugin(self, _plugin_name):
    return PluginManager.share_plugin(_plugin_name)
