from pydantic import BaseModel


class WalletHistoryBase(BaseModel):
    wallet_id: int
    old_balance: int
    new_balance: int


class WalletHistoryCreate(WalletHistoryBase):
    pass
