from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    category_id: int
    stock: int = Field(..., ge=0)   # ✅ MUST be >= 0


class ProductResponse(BaseModel):
    id: int
    name: str
    category_id: Optional[int] = None
    stock: int   # ✅ ADD THIS


    class Config:
        from_attributes = True
