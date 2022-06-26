import logging

from aiohttp import web
from marshmallow import ValidationError

from schema import ShopUnitImportRequest


routes = web.RouteTableDef()

log = logging.getLogger(__name__)


@routes.post("/imports")
async def imports(request):
    data = dict()
    body = await request.json()
    log.debug(f"imports(): request body: {body}")
    try:
        ShopUnitImportRequest().load(body)
    except ValidationError as err:
        log.info(f"ValidationError: {err.messages}")
        log.info(f"valid data: {err.valid_data}")
        return web.json_response(
            {"code": 400, "message": "Validation Failed"}, status=400
        )
    ...
    return web.json_response(data, status=200)


@routes.delete("/delete")
async def delete(request):
    data = dict()
    ...
    return web.json_response(data, status=200)


@routes.get("/nodes/{id}")
async def get(request):
    data = dict()
    ...
    return web.json_response(data, status=200)


def run_app():
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app)


if __name__ == "__main__":
    run_app()
