from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

# Import Product so SQLAlchemy knows about the products table
from app.models.product import Product


class PriceHistory(Base):
    # Tell SQLAlchemy that this model represents the price_history table
    __tablename__ = "price_history"

    # Store the unique ID of this price history record
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # Store the ID of the product associated with this price
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    # Store the price observed during this check
    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # Store whether the product was available during this check
    available: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    # Store when this price was observed
    checked_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )