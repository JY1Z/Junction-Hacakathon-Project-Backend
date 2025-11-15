# app/models/models
from sqlalchemy import Column, Integer, String, Boolean, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)  # JSON: what kind of kitchen
    behavior = Column(Text, nullable=True)  # JSON: history data
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    # items: JSON
    # items.id = product.id
    # status default: ordered, after checked: available / unavailable
    # [
    #   {"id": 1 , "name": "...", "quantity": 2, "status": "ordered", "price": 3.5},
    #
    # ]
    items = Column(Text, nullable=False, default="[]")

    status = Column(String, default="ordered")  # ordered / analyzed / confirmed ...
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("Customer", backref="orders")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=True)
    in_stock = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    sender_role = Column(String, nullable=False)          # "customer" / "delivery" / "system" / "admin"
    confirmation_status = Column(String, nullable=True)   # "agree" / "disagree" / None
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", backref="messages")
    customer = relationship("Customer", backref="messages")