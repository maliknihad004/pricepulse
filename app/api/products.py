from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from scraper import scrape_product

from app.repositories.product_repository import (
    create_product,
    get_all_products,
    get_product_by_id,
    delete_product,
    update_product_target_price,
)


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


class ProductCreate(BaseModel):
    url: str
    target_price: float


class ProductUpdate(BaseModel):
    target_price: float


def product_response(product):
    return {
        "id": product.id,
        "name": product.name,
        "url": product.url,
        "image_url": product.image_url,
        "target_price": product.target_price,
        "current_price": product.current_price,
        "available": product.available,
    }


@router.post("/")
def add_product(product_data: ProductCreate):

    # -------------------------
    # SCRAPE PRODUCT
    # -------------------------

    try:
        scraped_product = scrape_product(product_data.url)

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Could not scrape product: {error}",
        )

    # -------------------------
    # SAVE PRODUCT
    # -------------------------

    try:
        product = create_product(
            name=scraped_product["name"],
            url=product_data.url,
            image_url=scraped_product["image_url"],
            target_price=product_data.target_price,
            current_price=scraped_product["price"],
            available=scraped_product["available"],
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Could not save product: {error}",
        )

    # -------------------------
    # DUPLICATE PRODUCT
    # -------------------------

    if product is None:
        raise HTTPException(
            status_code=409,
            detail="This product is already being tracked.",
        )

    return product_response(product)


# -------------------------
# GET ALL PRODUCTS
# -------------------------

@router.get("/")
def get_products():

    products = get_all_products()

    return [
        product_response(product)
        for product in products
    ]


# -------------------------
# GET ONE PRODUCT
# -------------------------

@router.get("/{product_id}")
def get_product(product_id: int):

    product = get_product_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {product_id} not found",
        )

    return product_response(product)


# -------------------------
# DELETE PRODUCT
# -------------------------

@router.delete("/{product_id}")
def remove_product(product_id: int):

    product = delete_product(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {product_id} not found",
        )

    return {
        "message": "Product deleted successfully",
        "id": product_id,
        "name": product.name,
    }


# -------------------------
# UPDATE TARGET PRICE
# -------------------------

@router.put("/{product_id}")
def update_product(
    product_id: int,
    product_data: ProductUpdate,
):

    # Prevent negative target prices
    if product_data.target_price < 0:
        raise HTTPException(
            status_code=400,
            detail="Target price cannot be negative.",
        )

    product = update_product_target_price(
        product_id=product_id,
        target_price=product_data.target_price,
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {product_id} not found",
        )

    return product_response(product)