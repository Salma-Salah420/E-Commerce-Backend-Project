from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.category import Category  # كان ناقص
from schemas.category import CategoryCreate, CategoryResponse
from auth_dependency import get_current_user, admin_only

router = APIRouter()
router = APIRouter(tags=["Categories"])
@router.post("/categories", response_model=CategoryResponse, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db), current_user: dict = Depends(admin_only)):
    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(Category).all()

@router.get("/categories/{id}", response_model=CategoryResponse)
def get_category(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/categories/{id}", response_model=CategoryResponse)
def update_category(id: int, category: CategoryCreate, db: Session = Depends(get_db), current_user: dict = Depends(admin_only)):
    existing = db.query(Category).filter(Category.id == id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Category not found")
    existing.name = category.name
    db.commit()
    db.refresh(existing)
    return existing

@router.delete("/categories/{id}", status_code=200)
def delete_category(id: int, db: Session = Depends(get_db), current_user: dict = Depends(admin_only)):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"message": "Deleted successfully"}
