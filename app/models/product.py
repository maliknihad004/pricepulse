from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.database import Base


class Product(Base):
    __tablename__ = "products"

    # Primary key
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # Product name
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Product page URL
    url: Mapped[str] = mapped_column(
        String(2048),
        nullable=False,
    )

    # Product image URL
    image_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # User's target price
    target_price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # Latest scraped price
    current_price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    # Product availability
    available: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    # Whether an alert has already been sent
    target_alert_sent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Creation time
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    # Last update time
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )