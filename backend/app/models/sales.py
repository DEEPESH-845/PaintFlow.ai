from __future__ import annotations
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from app.database import Base


class SalesHistory(Base):
    __tablename__ = "sales_history"

    id = Column(Integer, primary_key=True, index=True)
    sku_id = Column(Integer, ForeignKey("skus.id"), nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    date = Column(Date, nullable=False)
    quantity_sold = Column(Integer, nullable=False, default=0)
    revenue = Column(Float, nullable=False, default=0.0)
    channel = Column(String, default="dealer")  # dealer, online, institutional
