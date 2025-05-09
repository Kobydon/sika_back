"""empty message

Revision ID: 6e9b2c6b0052
Revises: ee9a8b8cbba7
Create Date: 2024-02-16 12:56:55.447383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e9b2c6b0052'
down_revision = 'ee9a8b8cbba7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rooms', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_booked', sa.String(length=400), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rooms', schema=None) as batch_op:
        batch_op.drop_column('date_booked')

    # ### end Alembic commands ###
