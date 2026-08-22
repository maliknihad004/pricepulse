from app.repositories.price_history_repository import get_latest_price_history


def main():
    # Get the most recent price recorded for product ID 1
    history = get_latest_price_history(product_id=1)

    # Check whether price history exists for the product
    if history is not None:
        # Display the latest recorded price
        print(f"Latest price: ${history.price}")

        # Display when that price was recorded
        print(f"Checked at: {history.checked_at}")
    else:
        # Display a message when no price history exists
        print("No price history found.")


# Run the main function when this file is executed directly
if __name__ == "__main__":
    main()