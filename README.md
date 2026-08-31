# PricePulse

PricePulse is a price tracking application that monitors product prices, stores price history, and sends a Discord notification when a product reaches its target price.

The project includes automated tests, Docker-based deployment, and a Jenkins CI/CD pipeline.

## Features

* Add and manage products
* Track current product prices
* Store product price history
* Detect price changes and price drops
* Set a target price for a product
* Check whether a product reaches its target price
* Send Discord notifications for target-price alerts
* Prevent duplicate alerts while a product remains below its target price
* Automated tests with Pytest

## Tech Stack

* Python
* PostgreSQL
* SQLAlchemy
* Pytest
* Docker
* Docker Compose
* Jenkins
* GitHub Webhooks
* ngrok

## Testing

The project includes tests for database connectivity, scraping, target-price checks, and price comparison logic.

Run the tests with:

```bash
python -m pytest -v
```

## CI/CD

The project uses Jenkins to automate testing and deployment.

The pipeline:

1. Checks the required environment
2. Installs Python dependencies
3. Sets up the required environment variables
4. Runs the test suite
5. Deploys the application with Docker Compose if the tests pass

GitHub webhooks, exposed through ngrok, can trigger the Jenkins pipeline when changes are pushed to the repository.

## Running with Docker

```bash
docker compose up -d --build
```

To check running containers:

```bash
docker compose ps
```

To stop the application:

```bash
docker compose down
```

## Author

**Malik Hamdan**
