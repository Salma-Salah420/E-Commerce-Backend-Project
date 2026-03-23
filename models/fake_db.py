# ============================================================
# fake_db.py — Temporary in-memory storage for development
# ============================================================
# TODO: Replace all dictionaries below with actual SQLAlchemy
#       models and a real database (e.g., PostgreSQL via asyncpg).
# TODO: Replace FAKE_PRODUCTS with a database query:
#       product = db.query(Product).filter(Product.id == product_id).first()
# ============================================================

from typing import Dict

# ---------------------------------------------------------------------------
# Fake Product Catalog
# ---------------------------------------------------------------------------
# Simulates what will eventually be a Product table in the database.
# Each entry represents: { id: int, name: str, price: float, stock: int }
#
# TODO: Remove this dict and query the real Product model instead.
# Compatible shape with future Product model: id, price, stock (+ name, etc.)
# ---------------------------------------------------------------------------
FAKE_PRODUCTS: Dict[int, dict] = {
    1: {"id": 1, "name": "Laptop",       "price": 999.99, "stock": 10},
    2: {"id": 2, "name": "Headphones",   "price":  49.99, "stock":  5},
    3: {"id": 3, "name": "USB-C Hub",    "price":  29.99, "stock": 20},
    4: {"id": 4, "name": "Webcam",       "price":  79.99, "stock":  0},  # Out of stock
}

# ---------------------------------------------------------------------------
# In-Memory Cart Storage
# ---------------------------------------------------------------------------
# carts_db:      { user_id -> Cart dict }
# cart_items_db: { item_id -> CartItem dict }
#
# TODO: Replace with SQLAlchemy ORM models (Cart, CartItem tables).
# ---------------------------------------------------------------------------
carts_db: Dict[int, dict] = {}
cart_items_db: Dict[int, dict] = {}

# Auto-increment counters (simulating DB primary keys)
_cart_id_counter: int = 1
_item_id_counter: int = 1


def next_cart_id() -> int:
    global _cart_id_counter
    cid = _cart_id_counter
    _cart_id_counter += 1
    return cid


def next_item_id() -> int:
    global _item_id_counter
    iid = _item_id_counter
    _item_id_counter += 1
    return iid
