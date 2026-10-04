from pydantic import BaseModel, Field

class OrderItem(BaseModel):
    isbn: str
    quantity: int = Field(gt=0)

class OrderRequest(BaseModel):
    customer_id: int | None = None
    items: list[OrderItem] = Field(min_length=1)

class LoginRequest(BaseModel):
    user_name: str
    password: str