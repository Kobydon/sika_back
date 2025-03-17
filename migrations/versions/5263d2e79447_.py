"""empty message

Revision ID: 5263d2e79447
Revises: ee53a895e369
Create Date: 2024-02-09 16:44:18.048496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5263d2e79447'
down_revision = 'ee53a895e369'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('refund', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=400), nullable=True))
        batch_op.drop_column('description')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('refund', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.VARCHAR(length=400), nullable=True))
        batch_op.drop_column('status')

    # ### end Alembic commands ###
