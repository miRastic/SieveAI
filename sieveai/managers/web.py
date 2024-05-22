from .base import ManagerBase
from flask import Flask
import signal as Signal
import threading as Threader

class WebManager(ManagerBase):
  webapp_name = 'SieveAI-Web-Server'
  webapp_host = '127.0.0.1'
  webapp_port = '5007'
  webapp_debug = True
  webapp = None

  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
    self.webapp = Flask(self.webapp_name)

  def add_endpoint(self, _endpoint, _handler):
    self.webapp.route(_endpoint)(_handler)

  server_thread = None
  def serve(self, *args, **kwargs):
    _host = kwargs.get('host', args[0] if len(args) > 0 else self.webapp_host)
    _port = kwargs.get('port', args[1] if len(args) > 1 else self.webapp_port)
    _debug = kwargs.get('debug', args[2] if len(args) > 2 else self.webapp_debug)
    _reloader = kwargs.get('reloader', args[3] if len(args) > 3 else False)

    self.log_debug(f'Server Started at {_host}:{_port}')

    def _multi_serve():
      self.webapp.run(host=_host, port=_port, debug=_debug, use_reloader=_reloader)

    self.server_thread = Threader.Thread(target=_multi_serve)
    self.server_thread.start()
    self.log_debug(f'Server Started at {_host}:{_port}')

  def _shutdown(self):
    if self.server_thread:
      self.log_debug("Shutting down server...")
      self.server_thread.join()

  def setup_signal_handlers(self):
    Signal.signal(Signal.SIGINT, self._handle_signal)
    Signal.signal(Signal.SIGTERM, self._handle_signal)

  def _handle_signal(self, signum, frame):
    self._shutdown()

class SieveAIAPI(WebManager):
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def api_base(self, *args, **kwargs):
    return {
      'comment': 'Dynamic Route for Non-specific use case',
      'args': args,
      'kwargs': kwargs,
    }

  def api_welcome(self, *args, **kwargs):
    return {
      'hello': 'Welcome Back',
      'args': args,
      'kwargs': kwargs,
    }

  def api_introduction(self, *args, **kwargs):
    return {
      'hello': 'Visit some other website',
      'args': args,
      'kwargs': kwargs,
    }

  def method_endpoint_maps(self):
    return {
      '/': self.api_base,
      '<path:path>': self.api_base,
      'welcome': self.api_welcome,
      'intro': self.api_introduction,
    }

  def run_server(self):
    _ep_methods = self.method_endpoint_maps() or {}
    for _ep, _h in _ep_methods.items():
      if not _ep.startswith('/'):
        _ep = f"/{_ep}"
      self.add_endpoint(_ep, _h)

    self.setup_signal_handlers()
    self.serve()
