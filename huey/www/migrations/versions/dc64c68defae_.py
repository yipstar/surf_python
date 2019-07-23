"""empty message

Revision ID: dc64c68defae
Revises: 5bf05499726b
Create Date: 2019-07-13 18:16:08.432850

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'dc64c68defae'
down_revision = '5bf05499726b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('raw_spectral_wave_data',
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
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('raw_spectral_wave_data')
    # ### end Alembic commands ###
