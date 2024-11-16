from marshmallow import Schema, fields

class articleSchema(Schema):
    id = fields.Int(dump_only=True)



article_schema = articleSchema()
articles_schema = articleSchema(many=True)


    