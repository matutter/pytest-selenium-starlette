from selenium.webdriver.remote.webelement import WebElement
from tests.fixtures import *
import json

@pytest.fixture
async def server(app) -> Server:
  server = Server(app)
  server.start()
  await asyncio.sleep(0.1)
  yield server
  server.stop()
  await asyncio.sleep(0.1)


def get_element_by_id(driver: Chrome, id: str, timeout: float = 5.0) -> WebElement:

  loop = asyncio.get_event_loop()
  now = loop.time()
  end = now + timeout

  while now < end:
    try:
      el = driver.find_element_by_id(id)
      if el:
        return el
    except:
      pass
    now = loop.time()
  raise TimeoutError(f'failed to find element id={id} in {timeout}s')

async def test_browse_with_chrome_1(chrome: Chrome, server: Server):
  browser = chrome
  browser.get(server.url_for('/'))

  el = get_element_by_id(chrome, 'test-target')

  json_text = el.text
  data = json.loads(json_text)
  print(data)
  await asyncio.sleep(2)
