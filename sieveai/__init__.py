from .__metadata__ import __version__, __description__, __build__, __name__
from .managers import Manager

def dock():
  _m = Manager()
  _m.cli_dock()

def rescore():
  _m = Manager()
  _m.cli_rescore()
