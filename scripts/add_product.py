from app.repositories.product_repository import create_product


def main():
    # Define the product name
    name = "Gaming Mouse"

    # Define the product URL
    url = "https://example.com/product/gaming-mouse"

    # Define the product image URL
    image_url = "https://example.com/images/gaming-mouse.jpg"

    # Define the price at which the user wants an alert
    target_price = 30.00

    # Create the product in the database
    product = create_product(
        name=name,
        url=url,
        image_url=image_url,
        target_price=target_price,
        current_price=None,
        available=True,
    )

    # Check if the product already exists
    if product is None:
        print("Product with this URL already exists.")
        return

    # Display product information
    print(f"Product ID: {product.id}")
    print(f"Product: {product.name}")
    print(f"URL: {product.url}")
    print(f"Image URL: {product.image_url}")
    print(f"Target price: ${product.target_price:.2f}")


# Run the main function when this file is executed directly
if __name__ == "__main__":
    main()