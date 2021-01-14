from pydantic import BaseModel, validator
from typing import List


class WalletFields(BaseModel):
    user_id: int
    balance: int = 0

    @validator("balance")
    def check_balance(cls, v):
        if v < 0:
            raise ValueError("Incorrect balance")
        return v


class Wallet(WalletFields):
    id: int


class WalletReplenisment(BaseModel):
    amount: int

    @validator("amount")
    def check_balance(cls, v):
        if v < 0:
            raise ValueError("Incorrect amount")
        return v


class WalletsList(BaseModel):
    wallets: List[Wallet]
