from pydantic import BaseModel


class WalletHistoryFields(BaseModel):
    wallet_id: int
    old_balance: int
    new_balance: int
