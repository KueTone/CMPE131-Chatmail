"""users table

Revision ID: 5efa8b1f8844
Revises: 
Create Date: 2023-05-05 13:43:31.500586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5efa8b1f8844'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('last', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('bio', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('bio')
        batch_op.drop_column('age')
        batch_op.drop_column('last')
        batch_op.drop_column('first')

    # ### end Alembic commands ###
