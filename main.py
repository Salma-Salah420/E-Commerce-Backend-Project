# ============================================================
# main.py — FastAPI application entry point
# ============================================================
# Registers all routers and configures the app.
#
# TODO: Add JWT middleware / auth router when integrating auth module
# TODO: Add database connection lifespan events (startup/shutdown)
# TODO: Add CORS middleware for frontend integration
# ============================================================

from fastapi import FastAPI
from routes.cart_routes import router as cart_router

app = FastAPI(
    title="E-Commerce API — Shopping Cart Module",
    description=(
        "Task 3: Shopping Cart implementation.\n\n"
        "**Note:** Currently uses in-memory fake data. "
        "Replace with real DB and JWT auth before production."
    ),
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# Register Routers
# ---------------------------------------------------------------------------
# TODO: Register auth_router, product_router, order_router here as well
app.include_router(cart_router)


# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "module": "Shopping Cart", "version": "0.1.0"}
