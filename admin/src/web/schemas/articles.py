from marshmallow import Schema, fields

class articleSchema(Schema):
    id = fields.Int(dump_only=True)
    fecha_publicacion = fields.Date(dump_only=True)
    titulo = fields.String(dump_only=True)
    copete = fields.String(dump_only=True)



article_schema = articleSchema()
articles_schema = articleSchema(many=True)


    