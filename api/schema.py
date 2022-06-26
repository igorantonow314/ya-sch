from marshmallow import Schema, fields, validates, validates_schema, ValidationError
from marshmallow.validate import OneOf, Range

from dateutil import parser


class ShopUnitImport(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    parentId = fields.Str(allow_none=True)
    type = fields.Str(validate=OneOf(["OFFER", "CATEGORY"]), required=True)
    price = fields.Int(validate=Range(min=0), allow_none=True)

    # @validates('id')
    # def validate_id(self, value):
    #     parend = db.get(value)
    #     if parend and parend.type == 'OFFER':
    #         raise ValidationError

    @validates_schema
    def validate_category(self, data, **kwargs):
        if data["type"] == "CATEGORY":
            if data.get("price") is not None:
                raise ValidationError("Price for category must be null")
        else:
            if data.get("price") is None:
                raise ValidationError("Price for offer must be not-null")


class ShopUnitImportRequest(Schema):
    items = fields.Nested(ShopUnitImport(many=True))
    updateDate = fields.Str()

    @validates("updateDate")
    def validate_date(self, value):
        try:
            parser.parse(value)
        except parser.ParseError:
            raise ValidationError("Error while parsing updateDate")

    # TODO: add verification for items!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
