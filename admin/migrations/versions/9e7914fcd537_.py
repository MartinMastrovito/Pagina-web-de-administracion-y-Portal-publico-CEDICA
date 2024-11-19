"""empty message

Revision ID: 9e7914fcd537
Revises: 372ed53c1895
Create Date: 2024-11-16 18:16:04.916662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e7914fcd537'
down_revision = '372ed53c1895'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('publicaciones',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fecha_publicacion', sa.Date(), nullable=True),
    sa.Column('fecha_creacion', sa.Date(), nullable=False),
    sa.Column('fecha_actualizacion', sa.Date(), nullable=True),
    sa.Column('titulo', sa.String(length=25), nullable=False),
    sa.Column('copete', sa.String(length=255), nullable=True),
    sa.Column('contenido', sa.Text(), nullable=False),
    sa.Column('autor_id', sa.Integer(), nullable=False),
    sa.Column('estado', sa.Enum('Borrador', 'Publicado', 'Archivado', name='estado_publicacion'), nullable=True),
    sa.ForeignKeyConstraint(['autor_id'], ['empleados.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('invoices', schema=None) as batch_op:
        batch_op.alter_column('j_a',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
        batch_op.alter_column('recipient',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
        batch_op.drop_constraint('invoices_j_a_fkey', type_='foreignkey')
        batch_op.drop_constraint('invoices_recipient_fkey', type_='foreignkey')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)

    with op.batch_alter_table('invoices', schema=None) as batch_op:
        batch_op.create_foreign_key('invoices_recipient_fkey', 'empleados', ['recipient'], ['id'])
        batch_op.create_foreign_key('invoices_j_a_fkey', 'JYA', ['j_a'], ['id'])
        batch_op.alter_column('recipient',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
        batch_op.alter_column('j_a',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)

    op.drop_table('publicaciones')
    # ### end Alembic commands ###
