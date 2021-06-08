from typing import Any, Awaitable, Callable
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse, Response
from starlette.routing import Mount, Route
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.staticfiles import StaticFiles


class MyApp(Starlette):
    pass


async def test_handler(request: Request) -> Response:
    # redirect to test page
    return RedirectResponse('/assets/test.html')


async def api_handler(request: Request) -> Response:
    data = await request.json()
    print('got data', data)
    return JSONResponse({'status': 'ok'})


class CustomMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: MyApp, test: str = None):
        super().__init__(app)
        assert test == 'test'

    async def dispatch(self, request, call_next):
        # do stuff for all requests
        response = await call_next(request)
        return response


def create_app() -> MyApp:

    middleware = [
        Middleware(CustomMiddleware, test='test')
    ]

    routes = [
        Route('/', test_handler),
        Route('/api', api_handler, methods=['POST']),
        Mount('/assets', app=StaticFiles(directory='assets'), name='assets')
    ]

    return MyApp(routes=routes, middleware=middleware)
