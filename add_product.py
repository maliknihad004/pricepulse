from app.repositories.product_repository import create_product


def main():
    # Define the name of the product
    name = "Gaming Mouse"

    # Define the URL of the product
    url = "https://example.com/product/gaming-mouse"

    # Define the price at which the user wants an alert
    target_price = 30.00

    # Create the product in the database
    product = create_product(
        name=name,
        url=url,
        target_price=target_price,
        current_price=None,
        available=True,
    )

    # Display the product ID
    print(f"Product ID: {product.id}")

    # Display the product name
    print(f"Product: {product.name}")

    # Display the product URL
    print(f"URL: {product.url}")

    # Display the target price
    print(f"Target price: ${product.target_price:.2f}")


# Run the main function when this file is executed directly
if __name__ == "__main__":
    main()