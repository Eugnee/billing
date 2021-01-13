import sqlalchemy as sa
from . import metadata

from .wallet import wallet_table


wallet_history_table = sa.Table(
    "wallet_history",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("wallet_id", sa.ForeignKey(wallet_table.c.id), nullable=False),
    sa.Column("old_balance", sa.BigInteger(), nullable=False),
    sa.Column("new_balance", sa.BigInteger(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.sql.func.now()),
)
