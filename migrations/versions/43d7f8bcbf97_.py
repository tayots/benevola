"""empty message

Revision ID: 43d7f8bcbf97
Revises: None
Create Date: 2016-02-29 16:20:03.801069

"""

# revision identifiers, used by Alembic.
revision = '43d7f8bcbf97'
down_revision = None

from alembic import op
import sqlalchemy as sa
import geoalchemy2


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('first_name', sa.String(length=100), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.Column('middle_name', sa.String(length=100), nullable=True),
    sa.Column('address', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('section',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('polygon', geoalchemy2.types.Geometry(geometry_type='POLYGON'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('block',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('section_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('polygon', geoalchemy2.types.Geometry(geometry_type='POLYGON'), nullable=False),
    sa.ForeignKeyConstraint(['section_id'], ['section.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lot',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('block_id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('polygon', geoalchemy2.types.Geometry(geometry_type='POLYGON'), nullable=False),
    sa.Column('remarks', sa.String(length=50), nullable=True),
    sa.Column('area', sa.String(length=10), nullable=True),
    sa.Column('date_purchased', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['block_id'], ['block.id'], ),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('deceased',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('first_name', sa.String(length=100), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.Column('middle_name', sa.String(length=100), nullable=True),
    sa.Column('lot_id', sa.Integer(), nullable=False),
    sa.Column('date_of_death', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['lot_id'], ['lot.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deceased')
    op.drop_table('lot')
    op.drop_table('block')
    op.drop_table('section')
    op.drop_table('client')
    ### end Alembic commands ###
