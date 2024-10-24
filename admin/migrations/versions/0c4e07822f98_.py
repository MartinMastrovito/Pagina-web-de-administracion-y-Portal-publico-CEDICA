"""Añadir columnas y claves foráneas a varias tablas

Revision ID: 0c4e07822f98
Revises: 
Create Date: 2024-10-24 11:18:06.675204

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = '0c4e07822f98'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Obtener la conexión actual
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    # Verificar si la columna 'debts' ya existe antes de agregarla
    columns = [col['name'] for col in inspector.get_columns('JYA')]
    if 'debts' not in columns:
        with op.batch_alter_table('JYA', schema=None) as batch_op:
            batch_op.add_column(sa.Column('debts', sa.Boolean(), nullable=True))

    # Verificar si las columnas ya existen antes de agregarlas
    columns = [col['name'] for col in inspector.get_columns('documentos')]
    with op.batch_alter_table('documentos', schema=None) as batch_op:
        if 'nombre_documento' not in columns:
            batch_op.add_column(sa.Column('nombre_documento', sa.String(length=255), nullable=False))
        if 'created_at' not in columns:
            batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))
        if 'jya_dni' not in columns:
            batch_op.add_column(sa.Column('jya_dni', sa.String(length=20), nullable=False))
        batch_op.alter_column('caballo_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.create_foreign_key(None, 'JYA', ['jya_dni'], ['dni'])
        if 'nombre' in columns:
            batch_op.drop_column('nombre')

    with op.batch_alter_table('invoices', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'JYA', ['j_a'], ['id'])

    columns = [col['name'] for col in inspector.get_columns('user')]
    with op.batch_alter_table('user', schema=None) as batch_op:
        if 'created_at' not in columns:
            batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('created_at')

    with op.batch_alter_table('invoices', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    with op.batch_alter_table('documentos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nombre', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('caballo_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('jya_dni')
        batch_op.drop_column('created_at')
        batch_op.drop_column('nombre_documento')

    with op.batch_alter_table('JYA', schema=None) as batch_op:
        batch_op.drop_column('debts')
    # ### end Alembic commands ###