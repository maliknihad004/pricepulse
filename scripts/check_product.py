from scraper import scrape_product

# Import the function used to find a product by its URL
from app.repositories.product_repository import get_product_by_url

# Import the function that handles price comparison and alerts
from app.services import check_price


def main():
    # Define the URL of the product we want to monitor
    product_url = "https://example.com/product/headphones"

    # Find the product in the database using its URL
    product = get_product_by_url(product_url)

    # Stop the program if the product does not exist in the database
    if product is None:
        print("Product not found in the database.")
        return

    # Scrape the latest product information from the HTML page
    scraped_product = scrape_product("test_product.html")

    # Display the product information returned by the scraper
    print(f"Product: {scraped_product['name']}")
    print(f"Current price: ${scraped_product['price']}")
    print(f"Available: {scraped_product['available']}")

    # Check the new price against the previous price and target price
    result = check_price(
        product_id=product.id,
        product_name=product.name,
        new_price=scraped_product["price"],
        available=scraped_product["available"],
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


# Run the main function when this file is executed directly
if __name__ == "__main__":
    main()