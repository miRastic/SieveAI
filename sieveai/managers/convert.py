from .base import ManagerBase

class Converter(ManagerBase):
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
