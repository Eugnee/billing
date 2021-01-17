from pydantic import BaseModel, PositiveInt, validator


class WalletBase(BaseModel):
    balance: int = 0

    @validator("balance")
    def check_balance(cls, v):
        if v < 0:
            raise ValueError("Incorrect balance")
        return v


class WalletCreate(WalletBase):
    user_id: int


class WalletUpdate(WalletBase):
    pass


class Wallet(WalletCreate):
    id: int


class WalletReplenisment(BaseModel):
    cents: PositiveInt
