from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.order import Order, OrderItem
from models.product import Product
from schemas.order import OrderCreate, OrderResponse
from auth_dependency import get_current_user, admin_only

router = APIRouter(tags=["Orders"])


@router.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if not order.items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item")

    # Validate all products and stock before making any changes
    for item in order.items:
        if item.quantity <= 0:
            raise HTTPException(status_code=400, detail=f"Quantity must be greater than 0 for product {item.product_id}")

        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product '{product.name}'. Available: {product.stock}"
            )

    # Create the order
    new_order = Order(user_id=current_user.id)
    db.add(new_order)
    db.flush()  # Get the order ID without committing

    # Create order items and reduce stock
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        product.stock -= item.quantity

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(order_item)

    db.commit()
    db.refresh(new_order)
    
    for item in new_order.items:
        item.product_name = item.product.name  # SQLAlchemy lazy-loads product here
    
    return new_order


@router.get("/orders/me", response_model=List[OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Order).filter(Order.user_id == current_user.id).all()


@router.get("/orders", response_model=List[OrderResponse])
def get_all_orders(
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_only)
):
    return db.query(Order).all()