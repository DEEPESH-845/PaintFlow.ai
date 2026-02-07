from __future__ import annotations
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # North, South, East, West, Central
    states = Column(String, nullable=False)  # JSON array

    warehouses = relationship("Warehouse", back_populates="region")
    dealers = relationship("Dealer", back_populates="region")


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    capacity_litres = Column(Integer, nullable=False)

    region = relationship("Region", back_populates="warehouses")
    inventory_levels = relationship("InventoryLevel", back_populates="warehouse")


class InventoryLevel(Base):
    __tablename__ = "inventory_levels"

    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    sku_id = Column(Integer, ForeignKey("skus.id"), nullable=False)
    current_stock = Column(Integer, nullable=False, default=0)
    reorder_point = Column(Integer, nullable=False, default=50)
    max_capacity = Column(Integer, nullable=False, default=5000)
    last_updated = Column(DateTime, default=datetime.utcnow)
    days_of_cover = Column(Float, nullable=False, default=0.0)

    warehouse = relationship("Warehouse", back_populates="inventory_levels")


class InventoryTransfer(Base):
    __tablename__ = "inventory_transfers"

    id = Column(Integer, primary_key=True, index=True)
    from_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    to_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    sku_id = Column(Integer, ForeignKey("skus.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="PENDING")  # PENDING, APPROVED, IN_TRANSIT, COMPLETED
    recommended_at = Column(DateTime, default=datetime.utcnow)
    reason = Column(String, nullable=True)

    from_warehouse = relationship("Warehouse", foreign_keys=[from_warehouse_id])
    to_warehouse = relationship("Warehouse", foreign_keys=[to_warehouse_id])
