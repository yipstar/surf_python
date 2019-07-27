"""create buoy table

Revision ID: 84a19a0f1043
Revises: 
Create Date: 2019-07-27 10:13:23.154714

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2


# revision identifiers, used by Alembic.
revision = '84a19a0f1043'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'buoy',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('station_id', sa.String(150), unique = True, nullable=False),
        sa.Column('name', sa.String(564), nullable=True),
        sa.Column('owner', sa.String(564), nullable=True),
        sa.Column('pgm', sa.String(564), nullable=True),
        sa.Column('station_type', sa.String(150), nullable=True),
        sa.Column('lat', sa.Float(), nullable=True),
        sa.Column('lng', sa.Float(), nullable=True),
        sa.Column('point', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326), nullable=True),

        sa.Column('elevation', sa.Float(), nullable=True),
        sa.Column('hull', sa.String(100), nullable=True),
        sa.Column('anemom_height', sa.Float(), nullable=True),

        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True)
    )

def downgrade():
    op.drop_table('buoy')
