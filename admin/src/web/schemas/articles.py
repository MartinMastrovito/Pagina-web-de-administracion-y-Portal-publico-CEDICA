from marshmallow import Schema, fields


class articleSchema(Schema):
    """Este es el esquema que se utiliza para cada noticia individual"""
    id = fields.Int(dump_only=True)
    fecha_publicacion = fields.Date(dump_only=True)
    fecha_actualizacion = fields.Date(dump_only=True)
    fecha_creacion = fields.Date(dump_only=True)
    titulo = fields.String(dump_only=True)
    copete = fields.String(dump_only=True)
    contenido = fields.String(dump_only=True)
    autor_id = fields.Integer(dump_only=True)



article_schema = articleSchema()
articles_schema = articleSchema(many=True)


    