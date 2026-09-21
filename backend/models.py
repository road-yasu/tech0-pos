from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import \
        BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE, \
        DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, \
        LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, \
        NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, \
        TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR
from datetime import date, datetime
from zoneinfo import ZoneInfo

class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = "customers"
    customer_id: Mapped[int] = mapped_column(
        INTEGER,
        primary_key=True,
        autoincrement=True,
    )
    customer_name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
    )
    phone_number: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
    )
    address: Mapped[str] = mapped_column(
        VARCHAR(500),
        nullable=False,
    )
    sex: Mapped[int] = mapped_column(
        TINYINT(1),
        nullable=False,
    )
    age: Mapped[int] = mapped_column(
        INTEGER(1),
        nullable=False,
    )
    discount_rate: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
    )

class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(
        INTEGER,
        primary_key=True,
        autoincrement=True,
    )
    user_name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
    )

class Tax(Base):
    __tablename__ = "tax"
    tax_id: Mapped[int] = mapped_column(
        INTEGER,
        primary_key=True,
        autoincrement=True,
    )
    tax_rate: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
    )
    start_at: Mapped[datetime] = mapped_column(
        DATETIME,
        nullable=False,
    )
    finish_at: Mapped[datetime] = mapped_column(
        DATETIME,
        nullable=False,
    )

class Book(Base):
    __tablename__ = "books"
    book_id: Mapped[int] = mapped_column(
        INTEGER,
        primary_key=True,
        autoincrement=True,
    )
    isbn: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
    )
    book_name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
    )
    price: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
    )

class Order(Base):
    __tablename__ = "orders"
    order_id: Mapped[int] = mapped_column(
        INTEGER,
        primary_key=True,
        autoincrement=True,
    )
    customer_id: Mapped[int] = mapped_column(
        INTEGER,
        ForeignKey("customers.customer_id"),
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        INTEGER,
        ForeignKey("users.user_id"),
        nullable=False,
    )
    ordered_at: Mapped[datetime] = mapped_column(
        DATETIME(timezone=True),
        nullable=False,
        default=lambda: datetime.now(ZoneInfo("Asia/Tokyo"))
    )
    subtotal: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
    )
    discount_rate: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
    )
    tax_rate: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
    )
    tax_amount: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
    )
    total_amount: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
    )

class OrderDetail(Base):
    __tablename__ = "order_details"
    detail_id: Mapped[int] = mapped_column(
        INTEGER,
        primary_key=True,
        autoincrement=True,
    )
    order_id: Mapped[int] = mapped_column(
        INTEGER,
        ForeignKey("orders.order_id"),
        nullable=False,
    )
    book_id: Mapped[int] = mapped_column(
        INTEGER,
        ForeignKey("books.book_id"),
        nullable=False,
    )
    price: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
    )