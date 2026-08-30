import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_product(url):
    # --------------------------------------------------
    # GET HTML
    # --------------------------------------------------

    if url.startswith(("http://", "https://")):
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/131.0 Safari/537.36"
                )
            },
        )

        response.raise_for_status()
        html = response.text

    else:
        with open(url, "r", encoding="utf-8") as file:
            html = file.read()

    soup = BeautifulSoup(html, "html.parser")

    # --------------------------------------------------
    # PRODUCT NAME
    # --------------------------------------------------

    name_element = soup.select_one(".product-name")

    if name_element is None:
        name_element = soup.select_one("h1")

    if name_element is None:
        name_element = soup.select_one(
            'meta[property="og:title"]'
        )

    # --------------------------------------------------
    # PRODUCT PRICE
    # --------------------------------------------------

    price_element = soup.select_one(".price")

    if price_element is None:
        price_element = soup.select_one(".price_color")

    if price_element is None:
        price_element = soup.select_one(
            'meta[property="product:price:amount"]'
        )

    # --------------------------------------------------
    # AVAILABILITY
    # --------------------------------------------------

    availability_element = soup.select_one(".availability")

    if availability_element is None:
        availability_element = soup.select_one(
            '[itemprop="availability"]'
        )

    # --------------------------------------------------
    # PRODUCT IMAGE
    # --------------------------------------------------

    image_element = soup.select_one(
        ".product-image img"
    )

    if image_element is None:
        image_element = soup.select_one(
            ".thumbnail img"
        )

    if image_element is None:
        image_element = soup.select_one(
            'meta[property="og:image"]'
        )

    if image_element is None:
        image_element = soup.select_one("img")

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------

    if name_element is None:
        raise ValueError(
            "Could not find the product name."
        )

    if price_element is None:
        raise ValueError(
            "Could not find the product price."
        )

    # Availability is optional for some websites.
    # If it doesn't exist, we'll assume unavailable/unknown.
    available = None

    # --------------------------------------------------
    # PRODUCT NAME
    # --------------------------------------------------

    if name_element.name == "meta":
        name = name_element.get("content", "").strip()
    else:
        name = name_element.get_text(strip=True)

    # --------------------------------------------------
    # PRODUCT PRICE
    # --------------------------------------------------

    if price_element.name == "meta":
        price_text = price_element.get("content", "")
    else:
        price_text = price_element.get_text(strip=True)

    price_text = (
        price_text
        .replace("£", "")
        .replace("$", "")
        .replace("€", "")
        .replace("Â", "")
        .strip()
    )

    # Handle prices such as "$49.99 USD"
    import re

    price_match = re.search(
        r"\d+(?:\.\d+)?",
        price_text
    )

    if not price_match:
        raise ValueError(
            f"Could not parse product price: {price_text}"
        )

    price = float(price_match.group())

    # --------------------------------------------------
    # AVAILABILITY
    # --------------------------------------------------

    if availability_element is not None:

        if availability_element.name == "meta":
            availability = (
                availability_element.get(
                    "content",
                    ""
                )
            )
        else:
            availability = (
                availability_element
                .get_text(" ", strip=True)
            )

        available = (
            "in stock" in availability.lower()
            or "available" in availability.lower()
        )

    # --------------------------------------------------
    # IMAGE URL
    # --------------------------------------------------

    image_url = None

    if image_element is not None:

        if image_element.name == "meta":
            image_url = image_element.get(
                "content"
            )
        else:
            image_url = (
                image_element.get("src")
                or image_element.get("data-src")
                or image_element.get("data-lazy-src")
                or image_element.get("data-original")
            )

    # Convert relative image URL to absolute URL
    if (
        image_url
        and url.startswith(
            ("http://", "https://")
        )
    ):
        image_url = urljoin(
            url,
            image_url
        )

    # --------------------------------------------------
    # RETURN
    # --------------------------------------------------

    return {
        "name": name,
        "price": price,
        "available": available,
        "image_url": image_url,
    }