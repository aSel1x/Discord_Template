"""empty message

Revision ID: fc2047725b64
Revises: 
Create Date: 2024-10-23 02:01:25.266201

"""
from typing import Sequence, Union

from alembic import op
import app
import sqlmodel
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc2047725b64'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('created_at', app.models.types.unix.Unixepoch(), nullable=False),
    sa.Column('updated_at', app.models.types.unix.Unixepoch(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('discord_id', sa.BigInteger(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('discord_id')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('wallet',
    sa.Column('created_at', app.models.types.unix.Unixepoch(), nullable=False),
    sa.Column('updated_at', app.models.types.unix.Unixepoch(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('balance', sa.Numeric(scale=2), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wallet_id'), 'wallet', ['id'], unique=False)
    op.create_table('transaction',
    sa.Column('created_at', app.models.types.unix.Unixepoch(), nullable=False),
    sa.Column('updated_at', app.models.types.unix.Unixepoch(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_wallet_id', sa.Integer(), nullable=False),
    sa.Column('to_wallet_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Numeric(scale=2), nullable=False),
    sa.ForeignKeyConstraint(['from_wallet_id'], ['wallet.id'], ),
    sa.ForeignKeyConstraint(['to_wallet_id'], ['wallet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transaction_id'), 'transaction', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transaction_id'), table_name='transaction')
    op.drop_table('transaction')
    op.drop_index(op.f('ix_wallet_id'), table_name='wallet')
    op.drop_table('wallet')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###