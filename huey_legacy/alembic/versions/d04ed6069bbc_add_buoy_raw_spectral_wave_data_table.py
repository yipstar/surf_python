"""Add buoy_raw_spectral_wave_data table

Revision ID: d04ed6069bbc
Revises: a326050edfa0
Create Date: 2019-07-27 10:40:07.474396

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd04ed6069bbc'
down_revision = 'a326050edfa0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('buoy_raw_spectral_wave_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('buoy_id', sa.Integer(), nullable=False),
    sa.Column('ts', sa.DateTime(timezone=True), nullable=False),
    sa.Column('sep_freq', sa.Float(), nullable=True),
    sa.Column('spec_x', postgresql.ARRAY(sa.Float()), nullable=True),
    sa.Column('spec_y', postgresql.ARRAY(sa.Float()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['buoy_id'], ['buoy.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('buoy_id', 'ts', name='unique_buoy_raw_spectral_wave_data_ts')
    )


def downgrade():
    op.drop_table('raw_spectral_wave_data')
