"""empty message

Revision ID: efbb72e10d94
Revises: ddcebdcc705d
Create Date: 2019-06-26 06:28:30.823398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efbb72e10d94'
down_revision = 'ddcebdcc705d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('buoy_realtime_wave_detail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('buoy_id', sa.Integer(), nullable=True),
    sa.Column('ts', sa.DateTime(timezone=True), nullable=True),
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
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('buoy_realtime_wave_detail')
    # ### end Alembic commands ###