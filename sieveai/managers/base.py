from ..plug import DictConfig, SieveAIBase

class ManagerBase(SieveAIBase):
  ObjDict = DictConfig
  name = 'SieveAI'
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
