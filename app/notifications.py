import os

import requests

from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv()


def send_price_alert(product_name, current_price, target_price):
    # Get the Discord webhook URL from the environment
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    # Stop if the webhook URL has not been configured
    if not webhook_url:
        print("DISCORD_WEBHOOK_URL is not configured.")
        return

    # Create the notification message
    message = (
        f"🚨 PRICE ALERT 🚨\n"
        f"{product_name} has reached your target price!\n"
        f"Current price: ${current_price:.2f}\n"
        f"Target price: ${target_price:.2f}"
    )

    # Create the JSON payload expected by Discord
    payload = {
        "content": message,
    }

    # Send the notification to Discord
    response = requests.post(
        webhook_url,
        json=payload,
        timeout=10,
    )

    # Raise an exception if Discord rejected the request
    response.raise_for_status()

    # Confirm that the notification was sent successfully
    print("Discord notification sent successfully.")