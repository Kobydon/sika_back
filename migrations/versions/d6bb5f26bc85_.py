"""empty message

Revision ID: d6bb5f26bc85
Revises: ecc88f8930ad
Create Date: 2024-02-09 15:02:23.497260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6bb5f26bc85'
down_revision = 'ecc88f8930ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('refund_amount', sa.String(length=400), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.drop_column('refund_amount')

    # ### end Alembic commands ###
