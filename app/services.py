from app.repositories.price_history_repository import (
    create_price_history,
    get_latest_price_history,
)

# Import functions used to update product information
from app.repositories.product_repository import (
    update_product_price,
    mark_target_alert_sent,
    reset_target_alert,
)

# Import the function used to send price alerts
from app.notifications import send_price_alert


def check_price(
    product_id,
    product_name,
    new_price,
    available,
    target_price,
):
    # Get the most recently recorded price for the product
    previous_history = get_latest_price_history(product_id)

    # Check whether this product has been checked before
    if previous_history is None:
        # There is no previous price to compare against
        result = {
            "price_changed": False,
            "price_dropped": False,
            "previous_price": None,
            "new_price": new_price,
            "difference": None,
        }

    else:
        # Get the previous price from the database
        previous_price = previous_history.price

        # Calculate the difference between the new and previous prices
        # Round to 2 decimal places to avoid floating-point precision issues
        difference = round(new_price - previous_price, 2)

        # Determine whether the price changed
        price_changed = difference != 0

        # Determine whether the price decreased
        price_dropped = difference < 0

        # Store the result of the price comparison
        result = {
            "price_changed": price_changed,
            "price_dropped": price_dropped,
            "previous_price": previous_price,
            "new_price": new_price,
            "difference": difference,
        }

    # Save the new price to the price history table
    create_price_history(
        product_id=product_id,
        price=new_price,
        available=available,
    )

    # Update the product with the latest information
    update_product_price(
        product_id=product_id,
        name=product_name,
        image_url=None,
        current_price=new_price,
        available=available,
    )

    # Check whether the new price reached the target price
    target_reached = check_target_price(
        current_price=new_price,
        target_price=target_price,
    )

    # Store whether the target price was reached
    result["target_reached"] = target_reached

    # Handle the target-price alert
    if target_reached:
        # Get the latest product state
        from app.repositories.product_repository import get_all_products

        products = get_all_products()

        # Find the current product
        product = next(
            product
            for product in products
            if product.id == product_id
        )

        # Only send an alert if one has not already been sent
        if not product.target_alert_sent:
            # Send the Discord notification
            send_price_alert(
                product_name=product_name,
                current_price=new_price,
                target_price=target_price,
            )

            # Remember that the alert has been sent
            mark_target_alert_sent(product_id)

    else:
        # Price is above the target, so allow a future alert
        reset_target_alert(product_id)

    # Return the complete price-check result
    return result


def check_target_price(current_price, target_price):
    # Check whether the current price has reached or gone below the target
    target_reached = current_price <= target_price

    # Return whether the target price was reached
    return target_reached