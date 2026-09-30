from pydantic import BaseModel, Field

class OrderItem(BaseModel):
    isbn: str
    price: int
    quantity: int = Field(gt=0)

class OrderRequest(BaseModel):
    customer_id: int | None = None
    user_id: int
    items: list[OrderItem] = Field(min_length=1)
