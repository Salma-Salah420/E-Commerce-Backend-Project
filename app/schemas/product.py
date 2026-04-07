from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    category_id: int


class ProductResponse(BaseModel):
    id: int
    name: str
    category_id: Optional[int] = None

    class Config:
        from_attributes = True