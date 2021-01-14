from pydantic import BaseModel, EmailStr


class UserFields(BaseModel):
    email: EmailStr
    name: str


class User(UserFields):
    id: int


class UserWithWallet(User):
    balance: int
    wallet_id: int
