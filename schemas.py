from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)


class ProductUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    quantity: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
