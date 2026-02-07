from __future__ import annotations
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Dealer(Base):
    __tablename__ = "dealers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    tier = Column(String, nullable=False, default="Silver")  # Platinum, Gold, Silver
    credit_limit = Column(Float, nullable=False, default=500000.0)
    performance_score = Column(Float, nullable=False, default=50.0)

    region = relationship("Region", back_populates="dealers")
    warehouse = relationship("Warehouse")
    orders = relationship("DealerOrder", back_populates="dealer")


class DealerOrder(Base):
    __tablename__ = "dealer_orders"

    id = Column(Integer, primary_key=True, index=True)
    dealer_id = Column(Integer, ForeignKey("dealers.id"), nullable=False)
    sku_id = Column(Integer, ForeignKey("skus.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False, default="placed")  # recommended, placed, confirmed, shipped, delivered
    is_ai_suggested = Column(Boolean, default=False)
    order_source = Column(String, default="manual")  # ai_recommendation, manual, auto_replenish
    savings_amount = Column(Float, default=0.0)

    dealer = relationship("Dealer", back_populates="orders")
