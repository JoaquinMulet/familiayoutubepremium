"""Initial migration

Revision ID: fbc6debd5c6c
Revises: 
Create Date: 2024-04-09 11:24:46.317716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbc6debd5c6c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('financial_event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_type', sa.String(length=50), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('paid', sa.Boolean(), nullable=True),
    sa.Column('payment_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('financial_event')
    # ### end Alembic commands ###
