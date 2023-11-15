from pydantic import BaseModel, validator, Field, EmailStr


class UserCreate(BaseModel):
    email: EmailStr = Field(examples=['auto@tube.com'])
    password: str
    first_name: str = Field(examples=['Mufasa'])
    account: str = Field(description='Account type, must be Youtuber or Editor', examples=['Youtuber or Editor'])

    @validator('account')
    def account_in_accounts(cls, account):
        accounts = ['Youtuber', 'Editor']
        if account not in accounts:
            raise ValueError(f'Account type must be {accounts[0]} or {accounts[1]}')
        return account


class UserResponse(BaseModel):
    email: str
    first_name: str
    account: str

    class config():
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
    first_name: str | None = None

