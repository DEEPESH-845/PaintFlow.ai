from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.database import Base
from datetime import datetime


class CustomerOrderRequest(Base):
    __tablename__ = "customer_order_requests"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    shade_id = Column(Integer, ForeignKey("shades.id"), nullable=False)
    size_preference = Column(String, default="4L")
    dealer_id = Column(Integer, ForeignKey("dealers.id"), nullable=False)
    status = Column(String, default="requested")  # requested, contacted, fulfilled
    created_at = Column(DateTime, default=datetime.utcnow)
