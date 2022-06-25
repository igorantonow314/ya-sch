from aiohttp import web

routes = web.RouteTableDef()


@routes.post("/imports")
async def imports(request):
    data = dict()
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
