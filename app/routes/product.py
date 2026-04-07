from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.product import Product
from schemas.product import ProductCreate, ProductResponse
from auth_dependency import get_current_user, admin_only

router = APIRouter()
router = APIRouter(tags=["Products"])
@router.post("/products", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: dict = Depends(admin_only)):
    new_product = Product(
        name=product.name,
        category_id=product.category_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/products", response_model=List[ProductResponse])
def get_products(
    category_id: Optional[int] = None,
    search: Optional[str] = None,       # filtering بالاسم
    page: int = 1,                       # pagination
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    query = db.query(Product)
    
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    
    # Pagination
    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size).all()

@router.get("/products/{id}", response_model=ProductResponse)
def get_product(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{id}", response_model=ProductResponse)
def update_product(id: int, product: ProductCreate, db: Session = Depends(get_db), current_user: dict = Depends(admin_only)):
    existing = db.query(Product).filter(Product.id == id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")
    existing.name = product.name
    existing.category_id = product.category_id
    db.commit()
    db.refresh(existing)
    return existing

@router.delete("/products/{id}", status_code=200)
def delete_product(id: int, db: Session = Depends(get_db), current_user: dict = Depends(admin_only)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Deleted successfully"}
