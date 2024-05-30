from .base import CoreBase

class Dock(CoreBase):
  process_type = 'docking'
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
