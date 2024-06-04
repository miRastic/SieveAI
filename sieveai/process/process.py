from .base import CoreBase

class Process(CoreBase):
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
