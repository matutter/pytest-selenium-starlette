"""
Download drivers:

- Chrome:	https://sites.google.com/a/chromium.org/chromedriver/downloads
- Edge:	https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
- Firefox:	https://github.com/mozilla/geckodriver/releases
- Safari:	https://webkit.org/blog/6900/webdriver-support-in-safari-10/

Set the environment $PATH to the directory with the driver binary.
"""


import asyncio
import os
import os.path as op
import signal
from multiprocessing import Process
from typing import Any, Dict
from unittest import mock

import pytest
import uvicorn
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

pytestmark = pytest.mark.asyncio


@pytest.fixture
def chromedriver():
  driver_dir = op.join(op.dirname(__file__), '../drivers')
  path = os.environ['PATH']
  with mock.patch.dict(os.environ, {"PATH": ":".join([driver_dir, path])}):
    yield


@pytest.fixture
async def chrome(chromedriver) -> Chrome:
  options = ChromeOptions()
  #options.headless = True
  driver = Chrome(options=options)

  try:
    yield driver
  finally:
    driver.close()

@pytest.fixture
async def app() -> Starlette:

  async def root_handler(request: Request) -> Response:
    html = "<html><body><h1>Test</h1></body></html>"
    return Response(html, headers={'Content-Type':'text/html'})

  routes = [Route('/', root_handler)]
  app = Starlette(routes=routes)
  return app

@pytest.fixture
async def client(app) -> AsyncClient:
  async with AsyncClient(app=app, base_url='http://test:8080') as cli, LifespanManager(app):
    yield cli


class Server:
  process: Process
  host: str
  port: int
  log_level: str
  app: Starlette

  def __init__(self, app:Starlette, host: str = '127.0.0.1', port: int = 8600, log_level: str = 'debug'):
    self.app = app
    self.host = host
    self.port = port
    self.log_level = log_level
    self.process = None

  @property
  def url(self) -> str:
    return f'http://{self.host}:{self.port}'

  @property
  def uvicorn_options(self) -> Dict[str, Any]:
    return {k:getattr(self,k) for k in ('host', 'port', 'log_level')}

  def url_for(self, path: str = '/') -> str:
    url = self.url + path
    return url

  def _uvicorn_run(self):
    app = self.app
    kwargs = self.uvicorn_options
    try:
      uvicorn.run(app, **kwargs)
    except Exception as e:
      print(e)

  def start(self) -> None:
    if self.process:
      return

    self.process = Process(target=self._uvicorn_run, daemon=True)
    self.process.start()

  def stop(self) -> None:
    if not self.process:
      return

    try:
      # Graceful shutdown
      os.kill(self.process.pid, signal.SIGTERM)
    except:
      pass
    finally:
      self.process = None



@pytest.fixture
async def server(app) -> Server:
  server = Server(app)
  server.start()
  await asyncio.sleep(0.1)
  yield server
  server.stop()
  await asyncio.sleep(0.1)

async def test_browse_with_chrome(chrome: Chrome, server: Server):
  browser = chrome
  browser.get(server.url_for('/'))
  await asyncio.sleep(3)

async def test_browse_with_chrome2(chrome: Chrome, server: Server):
  browser = chrome
  browser.get(server.url_for('/'))
  await asyncio.sleep(3)
