import requests

from bs4 import BeautifulSoup


def scrape_product(url):
    # Check whether the input is a real HTTP/HTTPS URL
    if url.startswith(("http://", "https://")):
        # Send an HTTP request to the product webpage
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
        )

        # Raise an exception if the request failed
        response.raise_for_status()

        # Get the HTML returned by the website
        html = response.text

    else:
        # Open a local HTML file
        with open(url, "r", encoding="utf-8") as file:
            # Read the HTML content
            html = file.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find the product name
    name_element = soup.select_one(".product-name")

    # If our test-page selector does not exist, try the Books to Scrape selector
    if name_element is None:
        name_element = soup.select_one("h1")

    # Find the product price
    price_element = soup.select_one(".price")

    # If our test-page selector does not exist, try the Books to Scrape selector
    if price_element is None:
        price_element = soup.select_one(".price_color")

    # Find the availability element
    availability_element = soup.select_one(".availability")

    # Make sure the product name was found
    if name_element is None:
        raise ValueError("Could not find the product name.")

    # Make sure the price was found
    if price_element is None:
        raise ValueError("Could not find the product price.")

    # Make sure availability was found
    if availability_element is None:
        raise ValueError("Could not find product availability.")

    # Extract the product name
    name = name_element.get_text(strip=True)

    # Extract the price text
    price_text = price_element.get_text(strip=True)

    # Remove common currency and encoding characters
    price_text = (
        price_text
        .replace("£", "")
        .replace("$", "")
        .replace("Â", "")
        .strip()
    )

    # Convert the cleaned price to a floating-point number
    price = float(price_text)

    # Extract the availability text
    availability = availability_element.get_text(" ", strip=True)

    # Determine whether the product is currently available
    available = "in stock" in availability.lower()

    # Return the scraped product information
    return {
        "name": name,
        "price": price,
        "available": available,
    }