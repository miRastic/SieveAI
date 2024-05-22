from ..base import DictConfig, SieveAIBase

class ManagerBase(SieveAIBase):
  ObjDict = DictConfig
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
