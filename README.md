# PricePulse

PricePulse is a Python backend service that monitors product prices, stores price history in PostgreSQL, and sends Discord notifications when products reach a target price.

## Features

* Product price monitoring
* Web scraping
* PostgreSQL database
* Price history tracking
* Target price alerts
* Discord notifications
* Scheduled monitoring
* FastAPI REST API

## Architecture

```text
FastAPI
   |
   v
PostgreSQL
   |
   v
Scheduler
   |
   v
Scraper
   |
   v
Price Check
   |
   v
Discord Alert
```

## API

| Method | Endpoint         | Description         |
| ------ | ---------------- | ------------------- |
| GET    | `/`              | Health check        |
| POST   | `/products/`     | Add product         |
| GET    | `/products/`     | List products       |
| GET    | `/products/{id}` | Get product         |
| PUT    | `/products/{id}` | Update target price |
| DELETE | `/products/{id}` | Delete product      |

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Technologies

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* BeautifulSoup
* APScheduler
* Discord Webhooks

## Running

Create the virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configure the required environment variables, then start the API:

```bash
uvicorn main:app --reload
```

Run a monitoring cycle:

```bash
python monitor.py
```

Start automatic monitoring:

```bash
python scheduler.py
```

## Project Structure

```text
pricepulse/
├── app/
│   ├── api/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── notifications.py
│   └── services.py
├── tests/
│   ├── test_database.py
│   ├── test_price_check.py
│   ├── test_real_scraper.py
│   ├── test_scraper.py
│   ├── test_target_price.py
│   └── test_product.html
├── scripts/
│   ├── add_product.py
│   ├── check_product.py
│   ├── find_product.py
│   ├── get_latest_price.py
│   ├── get_products.py
│   ├── insert_price_history.py
│   ├── insert_product.py
│   └── price_tracker.py
├── main.py
├── monitor.py
├── scheduler.py
├── scraper.py
├── create_tables.py
├── requirements.txt
└── README.md
```

## Author

Malik Hamdan
Computer Science Student, An-Najah National University
