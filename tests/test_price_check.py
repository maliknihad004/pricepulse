from app.services import check_price


def main():
    # Simulate a new price received from the scraper
    new_price = 69.99

    # Check the new price against the latest stored price
    result = check_price(
        product_id=1,
        new_price=new_price,
        available=True,
    )

    # Display the previous price
    print(f"Previous price: ${result['previous_price']}")

    # Display the new price
    print(f"New price: ${result['new_price']}")

    # Display the price difference
    print(f"Difference: ${result['difference']}")

    # Display whether the price dropped
    print(f"Price dropped: {result['price_dropped']}")


# Run the test when this file is executed directly
if __name__ == "__main__":
    main()