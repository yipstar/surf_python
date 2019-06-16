"""empty message

Revision ID: ddcebdcc705d
Revises: f8baa061edbf
Create Date: 2019-06-16 13:05:00.103625

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2


# revision identifiers, used by Alembic.
revision = 'ddcebdcc705d'
down_revision = 'f8baa061edbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('buoy', sa.Column('point', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('buoy', 'point')
    # ### end Alembic commands ###
