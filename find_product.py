from app.repositories.product_repository import get_product_by_url


def main():
    # Search for the product using its URL
    product = get_product_by_url(
        "https://example.com/product/headphones"
    )

    # Check whether the product was found
    if product is not None:
        # Display the product ID
        print(f"Product ID: {product.id}")

        # Display the product name
        print(f"Product name: {product.name}")

        # Display the current price stored in the database
        print(f"Current price: ${product.current_price}")

    else:
        # Display a message when the product does not exist
        print("Product not found.")


# Run the test when this file is executed directly
if __name__ == "__main__":
    main()