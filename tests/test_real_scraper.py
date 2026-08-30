from scraper import scrape_product


def test_scrape_local_product():
    product = scrape_product("tests/test_product.html")

    assert product["name"] == "Wireless Headphones"
    assert product["price"] == 69.99
    assert product["available"] is True