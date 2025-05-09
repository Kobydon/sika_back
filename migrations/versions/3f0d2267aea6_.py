"""empty message

Revision ID: 3f0d2267aea6
Revises: 3aa411435456
Create Date: 2024-01-31 12:49:08.578379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f0d2267aea6'
down_revision = '3aa411435456'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('balance', sa.String(length=400), nullable=True))

    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.drop_column('balance')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('balance', sa.VARCHAR(length=400), nullable=True))

    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.drop_column('balance')

    # ### end Alembic commands ###
