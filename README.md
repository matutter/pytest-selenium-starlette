# Starlette Selenium Example

An repository which demonstrates how to use selenium webdriver to test starlette
apps and access those apps via selenium to ensure the page loads as expected.

## Setup

Ensure `python3.8` and `python3.8-venv` are installed then run the following
commands to setup the project.

```bash
python3.8 -m venv .venv
source .venv/bin/activate
pip install requirements.txt
```

## Setup Tests

This example uses chrome. The version of `chromedriver` must match your version
of chrome. Use the link below and replace the file `drivers/chromedriver` with
the version which is compatible for your browser.

[chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)

## Running Tests

Run the commands below.

```
source .venv/bin/activate
py.test
```

### What does this test do?

This test starts a subprocess running a `starlette` app. Then in the main
process starts the selenium driver to load the web page hosted by the app.

The HTTP transactions look like this.

1. Client navigates to `/`.
2. The test starts looking for an element in the web-page with the `id="test-target"`.
3. Server redirects to `/assets/test.html`.
4. Client loads `test.html` and then loads `test_script.js`.
5. Client runs `test_script.js` which makes an XHR request to `/api` after 1 second.
6. Server response with a JSON, `{"status": "ok"}`.
7. The client puts that JSON in a new element with the `id="test-target"`.
8. Selenium fetches the element.
9. The test receives the element and decodes the JSON inside the element with `id="test-target"`.
