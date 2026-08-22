from app.repositories.product_repository import get_all_products

# Import the scraper used to extract product information
from scraper import scrape_product

# Import the service that compares prices and sends alerts
from app.services import check_price


def monitor_products():
    # Get all products currently stored in the database
    products = get_all_products()

    # Check whether there are any products to monitor
    if not products:
        # Display a message when no products exist
        print("No products to monitor.")

        # Stop the function
        return

    # Loop through every product in the database
    for product in products:
        # Display which product is currently stored in the database
        print(f"\nChecking: {product.name}")

        # Display the product URL
        print(f"URL: {product.url}")

        try:
            # Scrape the product webpage using the URL stored in the database
            scraped_product = scrape_product(product.url)

            # Display the name found by the scraper
            print(f"Scraped name: {scraped_product['name']}")

            # Display the newly scraped price
            print(f"Current price: ${scraped_product['price']:.2f}")

            # Display the availability status
            print(f"Available: {scraped_product['available']}")

            # Compare the new price with the previous price
            result = check_price(
                product_id=product.id,

                # Use the product name found by the scraper
                product_name=scraped_product["name"],

                # Use the newly scraped price
                new_price=scraped_product["price"],

                # Use the newly scraped availability
                available=scraped_product["available"],

                # Use the target price stored in the database
                target_price=product.target_price,
            )

            # Display the previous price
            print(f"Previous price: ${result['previous_price']}")

            # Display the price difference
            print(f"Difference: ${result['difference']}")

            # Display whether the price dropped
            print(f"Price dropped: {result['price_dropped']}")

            # Display whether the target price was reached
            print(f"Target reached: {result['target_reached']}")

        except Exception as error:
            # Display the error without stopping the other products
            print(f"Failed to check {product.name}: {error}")


# Run the monitoring process when this file is executed directly
if __name__ == "__main__":
    monitor_products()