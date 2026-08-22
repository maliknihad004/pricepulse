from app.repositories.product_repository import get_all_products


def main():
    # Retrieve all products currently being monitored
    products = get_all_products()

    # Display the number of products found
    print(f"Products found: {len(products)}")

    # Display information about every product
    for product in products:
        # Display the product ID
        print(f"ID: {product.id}")

        # Display the product name
        print(f"Name: {product.name}")

        # Display the product URL
        print(f"URL: {product.url}")

        # Display the target price
        print(f"Target price: ${product.target_price:.2f}")

        # Separate products in the output
        print("-" * 40)


# Run the main function when this file is executed directly
if __name__ == "__main__":
    main()