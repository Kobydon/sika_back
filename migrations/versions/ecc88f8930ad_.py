"""empty message

Revision ID: ecc88f8930ad
Revises: 3f0d2267aea6
Create Date: 2024-02-07 13:08:04.431065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecc88f8930ad'
down_revision = '3f0d2267aea6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone', sa.String(length=400), nullable=True))
        batch_op.add_column(sa.Column('email', sa.String(length=400), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.drop_column('email')
        batch_op.drop_column('phone')

    # ### end Alembic commands ###
