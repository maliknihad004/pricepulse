from app.repositories.price_history_repository import get_latest_price_history


def detect_price_change(product_id, new_price):
    # Get the most recently recorded price for the product
    latest_history = get_latest_price_history(product_id)

    # Check whether this product has any previous price history
    if latest_history is None:
        # There is no previous price to compare against
        return {
            "changed": False,
            "previous_price": None,
            "new_price": new_price,
            "difference": None,
        }

    # Get the previous price from the latest history record
    previous_price = latest_history.price

    # Calculate the difference between the new and previous prices
    difference = new_price - previous_price

    # Determine whether the price actually changed
    changed = difference != 0

    # Return all the information needed by the application
    return {
        "changed": changed,
        "previous_price": previous_price,
        "new_price": new_price,
        "difference": difference,
    }


def main():
    # Simulate a new price scraped from the website
    new_price = 69.99

    # Compare the new price with the latest stored price
    result = detect_price_change(
        product_id=1,
        new_price=new_price,
    )

    # Display the previous price
    print(f"Previous price: ${result['previous_price']}")

    # Display the new scraped price
    print(f"New price: ${result['new_price']}")

    # Display the price difference
    print(f"Difference: ${result['difference']}")


# Run the test when this file is executed directly
if __name__ == "__main__":
    main()