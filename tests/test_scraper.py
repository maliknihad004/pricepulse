from scraper import scrape_product


def main():
    # Scrape the local test HTML file
    product = scrape_product("test_product.html")

    # Display the scraped product
    print(product)


# Run the test when this file is executed directly
if __name__ == "__main__":
    main()