"""Profile

Revision ID: c66740165df3
Revises: 91ba329dc335
Create Date: 2025-03-05 18:51:33.824666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c66740165df3'
down_revision = '91ba329dc335'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dob', sa.Date(), nullable=False),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', 'OTHER', 'PREFER_NOT_TO_SAY', name='genderenum'), nullable=False),
    sa.Column('phone', sa.String(length=10), nullable=False),
    sa.Column('state', sa.String(length=100), nullable=False),
    sa.Column('zip_code', sa.String(length=10), nullable=False),
    sa.Column('blood_group', sa.Enum('A_POSITIVE', 'A_NEGATIVE', 'B_POSITIVE', 'B_NEGATIVE', 'AB_POSITIVE', 'AB_NEGATIVE', 'O_POSITIVE', 'O_NEGATIVE', name='bloodgroupenum'), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_profile_user_id'), ['user_id'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_profile_user_id'))

    op.drop_table('profile')
    # ### end Alembic commands ###
