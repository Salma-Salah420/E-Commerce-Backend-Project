from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.order import Order, OrderItem
from models.product import Product
from schemas.order import OrderCreate, OrderResponse
from auth_dependency import get_current_user, admin_only

router = APIRouter(tags=["Orders"])


# -- Create a new order (any authenticated user) --
@router.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Check order has at least one item
    if not order.items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item")

    # Validate products exist and have enough stock before making any changes
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product '{product.name}'. Available: {product.stock}"
            )

    # Create the order and link it to the current user
    new_order = Order(user_id=current_user["user_id"])
    db.add(new_order)
    db.flush()

    # Add items to the order and reduce stock
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
    return new_order


# --- Get orders for the current logged-in user ---
@router.get("/orders/me", response_model=List[OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Return 404 if user has no orders
    orders = db.query(Order).filter(Order.user_id == current_user["user_id"]).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return orders


# --- Get all orders (Admin only) ---
@router.get("/orders", response_model=List[OrderResponse])
def get_all_orders(
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_only)
):
    return db.query(Order).all()

# --- Get a single order by ID (Admin or order owner) ---
@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Check order exists
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Allow only admin or the order owner to view it
    if current_user["role"] != "admin" and order.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to view this order")

    return order

# --- Update order status (Admin only) ---
@router.put("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_only)
):
    # Validate status value
    valid_statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Choose from: {valid_statuses}")

    # Check order exists
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status
    db.commit()
    db.refresh(order)
    return order


# --- Delete an order ( the Admin only) ---
@router.delete("/orders/{order_id}", status_code=200)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_only)
):
    # Check order exists before deleting
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}
