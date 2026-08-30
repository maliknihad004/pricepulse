
import os
import time
from datetime import datetime, UTC

import requests
from dotenv import load_dotenv

from app.db.database import SessionLocal
from app.models.product import Product
from app.models.price_history import PriceHistory
from scraper import scrape_product


load_dotenv()

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def send_discord_alert(product, price):
    if not DISCORD_WEBHOOK_URL:
        print("Discord webhook is not configured.")
        return

    message = {
        "content": (
            f"🎯 **Price Alert!**\n\n"
            f"**{product.name}**\n"
            f"Current price: **${price:.2f}**\n"
            f"Target price: **${product.target_price:.2f}**\n\n"
            f"Your target price has been reached!\n"
            f"{product.url}"
        )
    }

    try:
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json=message,
            timeout=10,
        )

        response.raise_for_status()
        print(f"  Discord alert sent for {product.name}")

    except requests.RequestException as error:
        print(f"  Discord alert failed: {error}")


def track_products():
    session = SessionLocal()

    try:
        products = session.query(Product).all()

        if not products:
            print("No products to track.")
            return

        print(
            f"\n[{datetime.now():%Y-%m-%d %H:%M:%S}] "
            f"Checking {len(products)} product(s)..."
        )

        for product in products:
            print(f"\nChecking: {product.name}")

            try:
                scraped = scrape_product(product.url)

                old_price = product.current_price
                new_price = scraped["price"]

                product.name = scraped["name"]
                product.current_price = new_price
                product.available = scraped["available"]
                product.image_url = scraped["image_url"]
                product.updated_at = datetime.now(UTC)

                # Save price history
                history = PriceHistory(
                    product_id=product.id,
                    price=new_price,
                    checked_at=datetime.now(UTC),
                )

                session.add(history)

                print(f"  Old price: {old_price}")
                print(f"  New price: {new_price}")
                print(f"  Target:    {product.target_price}")
                print(f"  Available: {product.available}")

                # Target price reached
                if (
                    product.available
                    and new_price <= product.target_price
                    and not product.target_alert_sent
                ):
                    send_discord_alert(product, new_price)
                    product.target_alert_sent = True

                # Reset alert if price goes above target again
                elif new_price > product.target_price:
                    product.target_alert_sent = False

            except Exception as error:
                print(f"  Failed: {error}")

        session.commit()
        print("\nTracking cycle completed.")

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def run_tracker():
    print("===================================")
    print("      PricePulse Tracker Worker")
    print("===================================")
    print(f"Check interval: {CHECK_INTERVAL} seconds")

    while True:
        try:
            track_products()
        except Exception as error:
            print(f"Tracker cycle failed: {error}")

        print(
            f"\nSleeping for {CHECK_INTERVAL} seconds..."
        )

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run_tracker()

