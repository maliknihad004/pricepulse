from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Import the scraper used to extract product information
from scraper import scrape_product

# Import the repository functions used to manage products
from app.repositories.product_repository import (
    create_product,
    get_all_products,
    delete_product,
    update_product_target_price,
)


# Create a router for product-related endpoints
router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


class ProductCreate(BaseModel):
    # URL of the product that PricePulse should monitor
    url: str

    # Maximum price the user is willing to pay
    target_price: float


class ProductUpdate(BaseModel):
    # New target price for the product
    target_price: float


@router.post("/")
def add_product(product_data: ProductCreate):
    # Try to scrape the product webpage
    try:
        # Extract the product name, price, and availability
        scraped_product = scrape_product(product_data.url)

    except Exception as error:
        # Return a 400 error when the webpage cannot be scraped
        raise HTTPException(
            status_code=400,
            detail=f"Could not scrape product: {error}",
        )

    # Create the product in PostgreSQL
    product = create_product(
        name=scraped_product["name"],
        url=product_data.url,
        target_price=product_data.target_price,
        current_price=scraped_product["price"],
        available=scraped_product["available"],
    )

    # Return the product information
    return {
        "id": product.id,
        "name": product.name,
        "url": product.url,
        "target_price": product.target_price,
        "current_price": product.current_price,
        "available": product.available,
    }


@router.get("/")
def get_products():
    # Get all products currently stored in PostgreSQL
    products = get_all_products()

    # Return an empty list when there are no products
    if not products:
        return []

    # Convert the SQLAlchemy objects into JSON-friendly dictionaries
    return [
        {
            "id": product.id,
            "name": product.name,
            "url": product.url,
            "target_price": product.target_price,
            "current_price": product.current_price,
            "available": product.available,
        }
        for product in products
    ]


@router.get("/{product_id}")
def get_product(product_id: int):
    # Get all products from the database
    products = get_all_products()

    # Search for the requested product
    for product in products:
        if product.id == product_id:
            # Return the product information
            return {
                "id": product.id,
                "name": product.name,
                "url": product.url,
                "target_price": product.target_price,
                "current_price": product.current_price,
                "available": product.available,
            }

    # Return a 404 error if the product does not exist
    raise HTTPException(
        status_code=404,
        detail=f"Product with ID {product_id} not found",
    )


@router.delete("/{product_id}")
def remove_product(product_id: int):
    # Delete the product and its price history
    product = delete_product(product_id)

    # Check whether the product existed
    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {product_id} not found",
        )

    # Return a confirmation message
    return {
        "message": "Product deleted successfully",
        "id": product_id,
        "name": product.name,
    }


@router.put("/{product_id}")
def update_product(
    product_id: int,
    product_data: ProductUpdate,
):
    # Update the product's target price
    product = update_product_target_price(
        product_id=product_id,
        target_price=product_data.target_price,
    )

    # Check whether the product exists
    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {product_id} not found",
        )

    # Return the updated product information
    return {
        "id": product.id,
        "name": product.name,
        "url": product.url,
        "target_price": product.target_price,
        "current_price": product.current_price,
        "available": product.available,
    }