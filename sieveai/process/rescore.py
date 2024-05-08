from .base import CoreBase

class Rescore(CoreBase):
  settings = None
  process_type = 'rescoring'
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
