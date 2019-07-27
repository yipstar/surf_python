"""Add buoy_realtime_wave_detail table

Revision ID: a326050edfa0
Revises: 84a19a0f1043
Create Date: 2019-07-27 10:38:07.923666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a326050edfa0'
down_revision = '84a19a0f1043'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'buoy_realtime_wave_detail',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('buoy_id', sa.Integer(), nullable=False),
        sa.Column('ts', sa.DateTime(timezone=True), nullable=False),
        sa.Column('significant_wave_height', sa.Float(), nullable=True),
        sa.Column('swell_height', sa.Float(), nullable=True),
        sa.Column('swell_period', sa.Float(), nullable=True),
        sa.Column('swell_direction', sa.String(length=10), nullable=True),
        sa.Column('wind_wave_height', sa.Float(), nullable=True),
        sa.Column('wind_wave_period', sa.Float(), nullable=True),
        sa.Column('steepness', sa.String(length=50), nullable=True),
        sa.Column('average_wave_period', sa.Float(), nullable=True),
        sa.Column('dominant_wave_direction', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['buoy_id'], ['buoy.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('buoy_id', 'ts', name='unique_buoy_ts')
    )


def downgrade():
    op.drop_table('buoy_realtime_wave_detail')
