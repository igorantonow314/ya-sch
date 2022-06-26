import logging
from math import floor

from aiohttp import web
from dateutil import parser
from marshmallow import ValidationError

from .schema import ShopUnitImportRequest
from db.db import DB


routes = web.RouteTableDef()

log = logging.getLogger(__name__)

db = DB()


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
    for item in body["items"]:
        db.insert_or_update(date=parser.parse(body["updateDate"]), **item)
        db.update_date(id=item["id"], datetime=parser.parse(body["updateDate"]))
    return web.json_response(data, status=200)


@routes.delete("/delete")
async def delete(request):
    data = dict()
    ...
    return web.json_response(data, status=200)


def get_node_json(uuid, _add_childs_info=False):
    node = db.get(uuid)
    if not node:
        raise ValueError
    data = node.as_dict()
    children = db.get_children(uuid)
    if children:
        data["children"] = []
        ch_n = 0
        ch_sum = 0
        for child in children:
            c = get_node_json(child, _add_childs_info=True)
            ch_n += c.pop("childs_count")
            ch_sum += c.pop("childs_sum")
            data["children"].append(c)
        if data["type"] == "CATEGORY":
            data["price"] = floor(ch_sum / ch_n) if ch_n else 0
        if _add_childs_info:
            data["childs_count"] = ch_n
            data["childs_sum"] = ch_sum
    else:
        if data["type"] == "CATEGORY":
            data["children"] = []
            data["price"] = None
        else:
            data["children"] = None
        if _add_childs_info:
            if data["type"] == "CATEGORY":
                data["childs_count"] = 0
                data["childs_sum"] = 0
            else:
                data["childs_count"] = 1
                data["childs_sum"] = data["price"]
    return data


@routes.get("/nodes/{id}")
async def get(request):
    uuid = request.match_info["id"]
    if not db.get(uuid):
        return web.json_response({"code": 404, "message": "Item not found"}, status=404)
    data = get_node_json(uuid)
    return web.json_response(data, status=200)


def run_app():
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app)


if __name__ == "__main__":
    run_app()
