from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int


class UserWithWallet(User):
    balance: int
    wallet_id: int
