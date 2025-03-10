"""Remote phone form profile

Revision ID: 41514a39347d
Revises: cb731baeba31
Create Date: 2025-03-05 21:41:37.487941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41514a39347d'
down_revision = 'cb731baeba31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.drop_column('phone')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('is_admin',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('is_admin',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone', sa.VARCHAR(length=15), nullable=False))

    # ### end Alembic commands ###
