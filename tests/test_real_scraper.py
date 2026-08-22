from scraper import scrape_product


def main():
    # Define the URL of the demo product page
    url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

    # Scrape the product information from the webpage
    product = scrape_product(url)

    # Display the scraped product information
    print(product)


# Run the test when this file is executed directly
if __name__ == "__main__":
    main()