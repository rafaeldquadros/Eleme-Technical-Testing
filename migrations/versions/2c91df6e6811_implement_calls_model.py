"""Implement calls model

Revision ID: 2c91df6e6811
Revises: 468a9da8d667
Create Date: 2023-07-04 18:36:03.924660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c91df6e6811'
down_revision = '468a9da8d667'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('calls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('priority_level', sa.String(length=40), nullable=False),
    sa.Column('status', sa.String(length=40), nullable=False),
    sa.Column('setor', sa.Float(precision=2), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.Column('createdAt', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('calls')
    # ### end Alembic commands ###
