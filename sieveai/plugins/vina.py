
from .base import PluginBase
from ..managers import Structures

from vina import Vina # Python binding for AutoDock VINA

class Vina(PluginBase):
  is_ready = False
  plugin_name = "AutoDock VINA"
  process = ['docking']
  url = "https://autodock-vina.readthedocs.io/en/latest/docking_python.html"

  Receptors = None
  Ligands = None

  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def setup(self, *args, **kwargs):
    self.update_attributes(self, kwargs)

  def boot(self, *args, **kwargs):
    self.setup(*args, **kwargs)
    ...

  def _prepare_receptor(self, _rec_id):
    ...

  def run(self, *args, **kwargs):
    ...

  def shutdown(self, *args, **kwargs):
    ...
