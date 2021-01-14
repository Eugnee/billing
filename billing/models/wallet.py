import sqlalchemy as sa
from sqlalchemy.sql.schema import CheckConstraint
from . import metadata

from .user import user_table


wallet_table = sa.Table(
    "wallet",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("user_id", sa.ForeignKey(user_table.c.id), unique=True, nullable=False),
    sa.Column("balance", sa.BigInteger(), default=0, comment="cents", nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.sql.func.now()),
    sa.Column("updated_at", sa.DateTime(timezone=True)),
    sa.Column(
        "is_active",
        sa.Boolean(),
        server_default=sa.sql.expression.true(),
        nullable=False,
    ),
    CheckConstraint("balance >= 0"),
)
