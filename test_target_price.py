from app.services import check_target_price


def main():
    # Set the current price returned by the scraper
    current_price = 79.99

    # Set the price the user wants to be notified about
    target_price = 70.00

    # Check whether the current price reached the target
    target_reached = check_target_price(
        current_price=current_price,
        target_price=target_price,
    )

    # Display the result
    print(f"Current price: ${current_price}")
    print(f"Target price: ${target_price}")
    print(f"Target reached: {target_reached}")


# Run the test when this file is executed directly
if __name__ == "__main__":
    main()