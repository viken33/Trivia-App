"""empty message

Revision ID: f5967304ae0a
Revises: 2f9009f2b624
Create Date: 2020-11-14 12:09:21.018874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5967304ae0a'
down_revision = '2f9009f2b624'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuario', sa.Column('highscore', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usuario', 'highscore')
    # ### end Alembic commands ###
