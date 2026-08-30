from scraper import scrape_product


def test_scrape_product():
    url = (
        "https://books.toscrape.com/"
        "catalogue/a-light-in-the-attic_1000/index.html"
    )

    product = scrape_product(url)

    assert product["name"]
    assert product["price"] > 0
    assert isinstance(product["available"], bool)