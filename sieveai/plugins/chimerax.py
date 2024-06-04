
from .base import PluginBase

class ChimeraX(PluginBase):
  is_ready = False
  plugin_name = "ChimeraX"
  process = ['analysis', 'conversion']
  url = "https://www.cgl.ucsf.edu/chimerax/docs/user/index.html"

  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
    self.require('requests', 'REQUESTS')
    self.require('json', 'JSON')

  def setup(self, *args, **kwargs):
    self.update_attributes(self, kwargs)

  def boot(self, *args, **kwargs):
    ...

  def run(self, *args, **kwargs):
    ...

  def shutdown(self, *args, **kwargs):
    ...

  def start_remote(self, *args, **kwargs) -> None:
    _start_chimerax = "chimerax --cmd 'remotecontrol rest start port 45385 json 1' &"
    self.OS.system(_start_chimerax)

  def request(self, *args, **kwargs):
    """
    Example: .request(params={"command": "surface #1; measure volume #1;"})

    """
    _url = kwargs.get("url", args[0] if len(args) > 0 else "http://127.0.0.1:45385/run")
    _params = kwargs.get("params", args[1] if len(args) > 1 else {})
    _return_type = kwargs.get("return_type", args[2] if len(args) > 2 else "json")
    _method = kwargs.get("method", args[3] if len(args) > 3 else 'get')

    if not _url:
      return None

    if _method == 'post':
      _r = self.REQUESTS.post(url=_url, data=self.JSON.dumps(_params))
    else:
      _r = self.REQUESTS.get(url=_url, params=_params)

    # Return other requests
    if _r.status_code == 200 and _return_type == 'json':
      _r = _r.json()

    return _r
