"""empty message

Revision ID: 10812df1eb61
Revises: 
Create Date: 2022-11-08 21:12:36.266729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10812df1eb61'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('username', sa.String(length=120), nullable=False),
    sa.Column('nombre', sa.String(length=120), nullable=False),
    sa.Column('apellido', sa.String(length=120), nullable=False),
    sa.Column('rut', sa.String(length=100), nullable=True),
    sa.Column('nombre_marca', sa.String(length=80), nullable=False),
    sa.Column('direccion', sa.String(length=250), nullable=False),
    sa.Column('descripcion', sa.String(length=250), nullable=False),
    sa.Column('tipo_pago', sa.String(length=250), nullable=False),
    sa.Column('banco_cuenta', sa.String(length=250), nullable=True),
    sa.Column('tipo_cuenta', sa.String(length=50), nullable=True),
    sa.Column('numero_cuenta', sa.Integer(), nullable=True),
    sa.Column('telefono', sa.String(length=12), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('nombre_marca'),
    sa.UniqueConstraint('username')
    )
    op.create_table('producto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vendedor', sa.Integer(), nullable=True),
    sa.Column('nombre_producto', sa.String(length=250), nullable=False),
    sa.Column('descripcion', sa.String(length=250), nullable=False),
    sa.Column('precio', sa.Integer(), nullable=False),
    sa.Column('url_foto', sa.String(length=250), nullable=True),
    sa.ForeignKeyConstraint(['vendedor'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('producto')
    op.drop_table('user')
    # ### end Alembic commands ###