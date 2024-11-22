"""empty message

Revision ID: d956ea0ce68b
Revises: 9e7914fcd537
Create Date: 2024-11-22 14:38:42.188048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd956ea0ce68b'
down_revision = '9e7914fcd537'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invoices', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ja_first_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('ja_last_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('recipient_first_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('recipient_last_name', sa.String(), nullable=True))
        batch_op.drop_column('j_a')
        batch_op.drop_column('recipient')

    with op.batch_alter_table('pago', schema=None) as batch_op:
        batch_op.add_column(sa.Column('beneficiario_nombre', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('beneficiario_apellido', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pago', schema=None) as batch_op:
        batch_op.drop_column('beneficiario_apellido')
        batch_op.drop_column('beneficiario_nombre')

    with op.batch_alter_table('invoices', schema=None) as batch_op:
        batch_op.add_column(sa.Column('recipient', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('j_a', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.drop_column('recipient_last_name')
        batch_op.drop_column('recipient_first_name')
        batch_op.drop_column('ja_last_name')
        batch_op.drop_column('ja_first_name')

    # ### end Alembic commands ###
