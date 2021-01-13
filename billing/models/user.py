import sqlalchemy as sa
from . import metadata


user_table = sa.Table(
    "user",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("email", sa.String(40), unique=True, index=True, nullable=False),
    sa.Column("name", sa.String(200), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.sql.func.now()),
    sa.Column("updated_at", sa.DateTime(timezone=True)),
    sa.Column(
        "is_active",
        sa.Boolean(),
        server_default=sa.sql.expression.true(),
        nullable=False,
    ),
)
