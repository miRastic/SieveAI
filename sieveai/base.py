
from UtilityLib import ObjDict as DictConfig, ProjectManager
from .__metadata__ import __version__, __build__

class SieveAIBase(ProjectManager):
  name = 'SieveAI'
  version = __version__
  def __init__(self, *args, **kwargs):
    print('Called Now...')
    super().__init__(**kwargs)

SieveAIBaseInit = SieveAIBase(name='DUMMYINIT')
