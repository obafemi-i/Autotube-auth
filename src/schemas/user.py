from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    # first_name: str


class UserResponse(BaseModel):
    email: str
    # first_name: str

    class config():
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
