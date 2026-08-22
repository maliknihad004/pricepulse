from fastapi import FastAPI

# Import the product API router
from app.api.products import router as product_router


# Create the FastAPI application
app = FastAPI(
    title="PricePulse API",
    description="API for tracking product prices",
    version="1.0.0",
)


# Register the product router with the FastAPI application
app.include_router(product_router)


@app.get("/")
def root():
    # Return a simple message to confirm that the API is running
    return {
        "message": "PricePulse API is running"
    }