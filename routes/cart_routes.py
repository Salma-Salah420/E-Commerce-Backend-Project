# ============================================================
# routes/cart_routes.py — API endpoints for the Shopping Cart
# ============================================================
# Thin layer: validates input via Pydantic schemas, then
# delegates ALL business logic to cart_service.py.
#
# Current auth: user_id is passed in the request body.
# TODO: Replace user_id body field with JWT dependency:
#
#   from fastapi import Depends
#   from auth.dependencies import get_current_user  # your JWT util
#
#   @router.get("/cart")
#   def get_cart(current_user = Depends(get_current_user)):
#       return cart_service.get_cart(current_user.id)
# ============================================================

from fastapi import APIRouter, status

from schemas.cart_schemas import (
    AddToCartRequest,
    UpdateCartItemRequest,
    CartResponse,
    MessageResponse,
)
from services import cart_service

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


# ---------------------------------------------------------------------------
# POST /cart — Add item to cart
# ---------------------------------------------------------------------------
@router.post(
    "/",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
    summary="Add a product to the cart",
    description=(
        "Adds a product to the user's cart. "
        "If the product already exists in the cart, quantity is incremented. "
        "Validates product existence and sufficient stock."
    ),
)
def add_to_cart(request: AddToCartRequest):
    """
    Add a product to the cart.

    - **user_id**: Temporary field. TODO: Replace with JWT current_user.id
    - **product_id**: Must be a valid product with available stock
    - **quantity**: Must be > 0
    """
    return cart_service.add_to_cart(
        user_id=request.user_id,
        product_id=request.product_id,
        quantity=request.quantity,
    )


# ---------------------------------------------------------------------------
# GET /cart — Get current user's cart
# ---------------------------------------------------------------------------
@router.get(
    "/",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
    summary="Get the current user's cart",
    description=(
        "Returns the full cart with all items, prices, subtotals, and total. "
        "Creates an empty cart if the user has none."
    ),
)
def get_cart(user_id: int):
    """
    Retrieve cart for a user.

    - **user_id**: Query param (temporary). TODO: Replace with JWT token extraction.
    """
    # TODO: Replace `user_id` query param with:
    #   current_user = Depends(get_current_user)
    #   return cart_service.get_cart(current_user.id)
    return cart_service.get_cart(user_id=user_id)


# ---------------------------------------------------------------------------
# PUT /cart/{item_id} — Update item quantity
# ---------------------------------------------------------------------------
@router.put(
    "/{item_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
    summary="Update quantity of a cart item",
    description=(
        "Updates the quantity of a specific item in the cart. "
        "Validates ownership and stock availability."
    ),
)
def update_cart_item(
    item_id: int,
    request: UpdateCartItemRequest,
    user_id: int,  # TODO: Replace with JWT dependency
):
    """
    Update a cart item's quantity.

    - **item_id**: Path param — the cart item to update
    - **quantity**: New quantity (must be > 0)
    - **user_id**: Query param (temporary). TODO: Extract from JWT.
    """
    return cart_service.update_cart_item(
        user_id=user_id,
        item_id=item_id,
        quantity=request.quantity,
    )


# ---------------------------------------------------------------------------
# DELETE /cart/clear — Clear entire cart
# ---------------------------------------------------------------------------
# ⚠️ IMPORTANT: This route MUST be defined BEFORE /{item_id}
#    to avoid FastAPI interpreting "clear" as an item_id integer.
# ---------------------------------------------------------------------------
@router.delete(
    "/clear",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Clear all items from the cart",
    description="Removes all items from the user's cart. The cart itself is kept.",
)
def clear_cart(user_id: int):
    """
    Clear the entire cart.

    - **user_id**: Query param (temporary). TODO: Extract from JWT.
    """
    return cart_service.clear_cart(user_id=user_id)


# ---------------------------------------------------------------------------
# DELETE /cart/{item_id} — Remove a single item
# ---------------------------------------------------------------------------
@router.delete(
    "/{item_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
    summary="Remove a specific item from the cart",
    description="Removes a single cart item by its ID. Validates ownership.",
)
def remove_from_cart(item_id: int, user_id: int):
    """
    Remove one item from the cart.

    - **item_id**: Path param — the cart item to remove
    - **user_id**: Query param (temporary). TODO: Extract from JWT.
    """
    return cart_service.remove_from_cart(user_id=user_id, item_id=item_id)
