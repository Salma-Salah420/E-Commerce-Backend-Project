# ============================================================
# schemas/cart_schemas.py — Pydantic models for request/response
# ============================================================
# These schemas handle input validation and response formatting.
# They are intentionally decoupled from the DB models so that
# future ORM model changes don't break the API contract.
# ============================================================

from pydantic import BaseModel, Field
from typing import List, Optional


# ---------------------------------------------------------------------------
# Request Schemas (Input)
# ---------------------------------------------------------------------------

class AddToCartRequest(BaseModel):
    """
    Payload for adding a product to the cart.

    TODO: Remove user_id from request body once JWT auth is integrated.
          Instead, extract user_id from the token: current_user.id
    """
    # TODO: Replace with JWT-authenticated user: user_id = current_user.id
    user_id: int = Field(..., description="ID of the user (temporary — will come from JWT)")
    product_id: int = Field(..., description="ID of the product to add")
    quantity: int = Field(..., gt=0, description="Quantity must be greater than 0")


class UpdateCartItemRequest(BaseModel):
    """Payload for updating quantity of an existing cart item."""
    quantity: int = Field(..., gt=0, description="New quantity — must be greater than 0")


# ---------------------------------------------------------------------------
# Response Schemas (Output)
# ---------------------------------------------------------------------------

class CartItemResponse(BaseModel):
    """Represents a single item in the cart (response shape)."""
    id: int
    cart_id: int
    product_id: int
    quantity: int
    price: float          # Price at time of adding (snapshot)
    subtotal: float       # quantity × price (computed field)

    # TODO: Optionally join product name from Product table for richer response
    # product_name: Optional[str] = None


class CartResponse(BaseModel):
    """Full cart response including all items and total."""
    id: int
    user_id: int
    items: List[CartItemResponse]
    total: float          # Sum of all item subtotals


class MessageResponse(BaseModel):
    """Generic success/info message."""
    message: str
    detail: Optional[str] = None
