from flask.ext.restful import fields
from app.utils.gis_json_fields import PolygonToLatLng

lot_fields = dict(
    id=fields.Integer,
    block_id=fields.Integer,
    client_id=fields.Integer,
    area=PolygonToLatLng(attribute='area'),
    dimension_width=fields.Float,
    dimension_height=fields.Float,
    lot_area=fields.Float,
    price_per_sq_mtr=fields.Float,
    date_purchased=fields.DateTime("iso8601"),
    status=fields.String,
    date_created=fields.DateTime("iso8601"),
    date_modified=fields.DateTime("iso8601")
)

lot_create_fields = dict(
    status=fields.String,
    message=fields.String,
    lot=fields.Nested(lot_fields, allow_null=False)
)