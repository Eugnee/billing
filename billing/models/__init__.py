import sqlalchemy as sa

metadata = sa.MetaData()

from .user import user_table
from .wallet import wallet_table
from .wallet_history import wallet_history_table
