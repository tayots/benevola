"""empty message

Revision ID: 5ab28d3f1722
Revises: 4072f2985ba4
Create Date: 2016-06-01 02:24:00.455246

"""

# revision identifiers, used by Alembic.
revision = '5ab28d3f1722'
down_revision = '4072f2985ba4'

from alembic import op
import sqlalchemy as sa
import geoalchemy2


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client', sa.Column('date_of_birth', sa.Date(), nullable=True))
    op.add_column('deceased', sa.Column('date_of_birth', sa.Date(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('deceased', 'date_of_birth')
    op.drop_column('client', 'date_of_birth')
    ### end Alembic commands ###
