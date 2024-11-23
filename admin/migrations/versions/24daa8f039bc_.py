"""empty message

Revision ID: 24daa8f039bc
Revises: 
Create Date: 2024-11-22 23:33:14.919543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24daa8f039bc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('JYA', schema=None) as batch_op:
        batch_op.alter_column('caballo_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('caballo_conductores', schema=None) as batch_op:
        batch_op.add_column(sa.Column('empleado_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'empleados', ['empleado_id'], ['id'])
        batch_op.drop_column('miembroequipo_id')

    with op.batch_alter_table('caballo_entrenadores', schema=None) as batch_op:
        batch_op.add_column(sa.Column('empleado_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'empleados', ['empleado_id'], ['id'])
        batch_op.drop_column('miembroequipo_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('caballo_entrenadores', schema=None) as batch_op:
        batch_op.add_column(sa.Column('miembroequipo_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('empleado_id')

    with op.batch_alter_table('caballo_conductores', schema=None) as batch_op:
        batch_op.add_column(sa.Column('miembroequipo_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('empleado_id')

    with op.batch_alter_table('JYA', schema=None) as batch_op:
        batch_op.alter_column('caballo_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
