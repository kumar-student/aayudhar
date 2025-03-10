"""Hospital

Revision ID: ffdd7be2a9e7
Revises: 90390c77effd
Create Date: 2025-03-06 21:34:06.133742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffdd7be2a9e7'
down_revision = '90390c77effd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hospital',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('image', sa.String(length=256), nullable=True),
    sa.Column('hrn', sa.String(length=32), nullable=False),
    sa.Column('address', sa.String(length=120), nullable=False),
    sa.Column('state', sa.String(length=100), nullable=False),
    sa.Column('zip_code', sa.String(length=10), nullable=False),
    sa.Column('phone', sa.String(length=10), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('phone')
    )
    with op.batch_alter_table('hospital', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_hospital_hrn'), ['hrn'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hospital', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_hospital_hrn'))

    op.drop_table('hospital')
    # ### end Alembic commands ###
