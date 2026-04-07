from pydantic import BaseModel

# 📥 البيانات اللي داخلة
class CategoryCreate(BaseModel):
    name: str


# 📤 البيانات اللي خارجة
class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True