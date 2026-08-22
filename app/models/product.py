from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Product(Base):
    # Tell SQLAlchemy that this model represents the products table
    __tablename__ = "products"

    # Store the unique identifier of the product
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # Store the product name
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Store the URL of the product page
    url: Mapped[str] = mapped_column(
        String(2048),
        nullable=False,
    )

    # Store the price at which the user wants to receive an alert
    target_price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # Store the most recently scraped price
    current_price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    # Store whether the product is currently available
    available: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    # Track whether a target-price alert has already been sent
    target_alert_sent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Store the time when the product was added
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    # Store the time when the product was last updated
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )