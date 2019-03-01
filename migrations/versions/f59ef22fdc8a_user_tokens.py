"""user tokens

Revision ID: f59ef22fdc8a
Revises: d3b74c88ef46
Create Date: 2019-03-01 12:58:00.466510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f59ef22fdc8a'
down_revision = 'd3b74c88ef46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('token', sa.String(length=32), nullable=True))
    op.add_column('user', sa.Column('token_expiration', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_column('user', 'token_expiration')
    op.drop_column('user', 'token')
    # ### end Alembic commands ###
