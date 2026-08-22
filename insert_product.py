from app.repositories.product_repository import create_product


def main():
    # Create a product using information that could have come from our scraper
    product = create_product(
        name="Wireless Headphones",
        url="https://example.com/product/headphones",
        target_price=70.00,
        current_price=79.99,
        available=True,
    )

    # Display the ID assigned to the product by PostgreSQL
    print(f"Product created with ID: {product.id}")


# Run the main function when this file is executed directly
if __name__ == "__main__":
    main()