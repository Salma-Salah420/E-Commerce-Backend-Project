# ============================================================
# services/cart_service.py — Core business logic for the cart
# ============================================================
# This service layer is the single source of truth for all
# cart operations. Routes delegate to these functions.
#
# Current state: uses in-memory fake_db for all storage.
#
# TODO (Integration checklist):
#   [ ] Replace fake_db lookups with SQLAlchemy db session queries
#   [ ] Replace user_id param with authenticated user from JWT
#   [ ] Connect CartItem.product_id to real Product FK relationship
#   [ ] Add checkout / order placement logic at the end of flow
# ============================================================

from fastapi import HTTPException, status
from typing import Optional

from models.fake_db import (
    FAKE_PRODUCTS,
    carts_db,
    cart_items_db,
    next_cart_id,
    next_item_id,
)
from schemas.cart_schemas import (
    CartItemResponse,
    CartResponse,
)


# ===========================================================================
# Internal Helpers
# ===========================================================================

def _get_product(product_id: int) -> dict:
    """
    Fetch a product by ID. Raises 404 if not found.

    TODO: Replace with:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
    """
    product = FAKE_PRODUCTS.get(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id={product_id} not found."
        )
    return product


def _get_or_create_cart(user_id: int) -> dict:
    """
    Returns the existing cart for a user, or creates a new one.

    TODO: Replace with:
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.add(cart); db.commit(); db.refresh(cart)
    """
    if user_id not in carts_db:
        cid = next_cart_id()
        carts_db[user_id] = {"id": cid, "user_id": user_id}
    return carts_db[user_id]


def _get_cart_items(cart_id: int) -> list:
    """Return all cart items that belong to the given cart_id."""
    return [item for item in cart_items_db.values() if item["cart_id"] == cart_id]


def _find_existing_item(cart_id: int, product_id: int) -> Optional[dict]:
    """
    Check if a product is already in the cart.
    Prevents duplicate entries — merges quantity instead.
    """
    for item in cart_items_db.values():
        if item["cart_id"] == cart_id and item["product_id"] == product_id:
            return item
    return None


def _get_item_or_404(item_id: int) -> dict:
    """Fetch a cart item by ID or raise 404."""
    item = cart_items_db.get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cart item with id={item_id} not found."
        )
    return item


def _build_cart_response(cart: dict) -> CartResponse:
    """
    Assembles a CartResponse from raw cart dict + its items.
    Calculates subtotal per item and total for the whole cart.
    """
    raw_items = _get_cart_items(cart["id"])
    item_responses = []

    for item in raw_items:
        subtotal = round(item["quantity"] * item["price"], 2)
        item_responses.append(
            CartItemResponse(
                id=item["id"],
                cart_id=item["cart_id"],
                product_id=item["product_id"],
                quantity=item["quantity"],
                price=item["price"],
                subtotal=subtotal,
            )
        )

    total = calculate_total(item_responses)

    return CartResponse(
        id=cart["id"],
        user_id=cart["user_id"],
        items=item_responses,
        total=total,
    )


# ===========================================================================
# Public Service Functions
# ===========================================================================

def add_to_cart(user_id: int, product_id: int, quantity: int) -> CartResponse:
    """
    Add a product to the user's cart.

    Business rules:
    - Product must exist
    - Product must have sufficient stock
    - quantity must be > 0 (enforced by schema)
    - If the product is already in cart → increment quantity (no duplicate)

    Args:
        user_id:    The authenticated user's ID.
                    TODO: Will come from JWT token (current_user.id)
        product_id: The product to add.
                    TODO: Will be validated against real Product FK
        quantity:   How many units to add.

    Returns:
        Updated CartResponse.
    """
    # 1. Validate product exists and has enough stock
    product = _get_product(product_id)

    if product["stock"] <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product '{product['name']}' is out of stock."
        )

    if quantity > product["stock"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Requested quantity ({quantity}) exceeds available stock "
                f"({product['stock']}) for '{product['name']}'."
            )
        )

    # 2. Get or create the user's cart
    cart = _get_or_create_cart(user_id)

    # 3. Check if product already exists in cart → update instead of duplicating
    existing_item = _find_existing_item(cart["id"], product_id)

    if existing_item:
        new_quantity = existing_item["quantity"] + quantity
        if new_quantity > product["stock"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Total quantity in cart ({new_quantity}) would exceed "
                    f"available stock ({product['stock']})."
                )
            )
        existing_item["quantity"] = new_quantity
    else:
        # 4. Create a new CartItem
        item_id = next_item_id()
        cart_items_db[item_id] = {
            "id": item_id,
            "cart_id": cart["id"],
            "product_id": product_id,
            "quantity": quantity,
            "price": product["price"],  # Snapshot price at time of adding
            # TODO: Connect to real Product FK: product_id → Product.id
        }

    return _build_cart_response(cart)


def get_cart(user_id: int) -> CartResponse:
    """
    Retrieve the current cart for a user.
    Returns an empty cart if the user has no active cart.

    Args:
        user_id: The authenticated user's ID.
                 TODO: Will come from JWT token (current_user.id)

    Returns:
        CartResponse (may have empty items list).
    """
    cart = _get_or_create_cart(user_id)
    return _build_cart_response(cart)


def update_cart_item(user_id: int, item_id: int, quantity: int) -> CartResponse:
    """
    Update the quantity of a specific cart item.

    Validates:
    - Item must exist
    - Item must belong to the requesting user's cart
    - New quantity must not exceed available stock

    Args:
        user_id:  The authenticated user (for ownership check).
                  TODO: Replace with current_user.id from JWT
        item_id:  The cart item to update.
        quantity: New quantity (must be > 0, enforced by schema).

    Returns:
        Updated CartResponse.
    """
    item = _get_item_or_404(item_id)

    # Ownership check: ensure the item belongs to this user's cart
    cart = _get_or_create_cart(user_id)
    if item["cart_id"] != cart["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify this cart item."
        )

    # Validate new quantity against current stock
    product = _get_product(item["product_id"])
    if quantity > product["stock"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Requested quantity ({quantity}) exceeds available stock "
                f"({product['stock']}) for '{product['name']}'."
            )
        )

    item["quantity"] = quantity
    return _build_cart_response(cart)


def remove_from_cart(user_id: int, item_id: int) -> CartResponse:
    """
    Remove a single item from the cart.

    Args:
        user_id: The authenticated user (for ownership check).
                 TODO: Replace with current_user.id from JWT
        item_id: The cart item to remove.

    Returns:
        Updated CartResponse after removal.
    """
    item = _get_item_or_404(item_id)

    # Ownership check
    cart = _get_or_create_cart(user_id)
    if item["cart_id"] != cart["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to remove this cart item."
        )

    del cart_items_db[item_id]
    return _build_cart_response(cart)


def clear_cart(user_id: int) -> dict:
    """
    Remove ALL items from the user's cart.
    The cart record itself remains (just emptied).

    Args:
        user_id: The authenticated user.
                 TODO: Replace with current_user.id from JWT

    Returns:
        Success message dict.
    """
    cart = _get_or_create_cart(user_id)
    items_to_delete = [
        iid for iid, item in cart_items_db.items()
        if item["cart_id"] == cart["id"]
    ]

    for iid in items_to_delete:
        del cart_items_db[iid]

    return {"message": "Cart cleared successfully.", "detail": f"Removed {len(items_to_delete)} item(s)."}


def calculate_total(items: list) -> float:
    """
    Calculate the total price of all items in the cart.

    Accepts a list of CartItemResponse objects (with subtotal field)
    or raw dicts with quantity and price.

    TODO: Add discount/coupon logic here when implementing checkout.
    TODO: Add tax calculation here if required.

    Returns:
        Rounded total as float.
    """
    total = 0.0
    for item in items:
        if hasattr(item, "subtotal"):
            total += item.subtotal
        else:
            total += item["quantity"] * item["price"]
    return round(total, 2)
