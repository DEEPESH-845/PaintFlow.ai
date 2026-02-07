from __future__ import annotations
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # Interior Wall, Exterior Wall, Wood & Metal, Waterproofing
    sub_category = Column(String, nullable=False)  # Premium, Economy, Luxury
    base_type = Column(String, nullable=False)  # Water-based, Oil-based
    finish = Column(String, nullable=False)  # Matt, Soft Sheen, High Gloss, Satin
    sizes_available = Column(Text, nullable=False)  # JSON array: ["1L","4L","10L","20L"]
    price_per_litre = Column(Float, nullable=False)

    shades = relationship("Shade", back_populates="product")


class Shade(Base):
    __tablename__ = "shades"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    shade_code = Column(String, unique=True, nullable=False)
    shade_name = Column(String, nullable=False)
    hex_color = Column(String, nullable=False)
    rgb_r = Column(Integer, nullable=False)
    rgb_g = Column(Integer, nullable=False)
    rgb_b = Column(Integer, nullable=False)
    shade_family = Column(String, nullable=False)  # Reds, Blues, Greens, Yellows, Neutrals, Whites
    is_trending = Column(Boolean, default=False)

    product = relationship("Product", back_populates="shades")
    skus = relationship("SKU", back_populates="shade")


class SKU(Base):
    __tablename__ = "skus"

    id = Column(Integer, primary_key=True, index=True)
    shade_id = Column(Integer, ForeignKey("shades.id"), nullable=False)
    size = Column(String, nullable=False)  # 1L, 4L, 10L, 20L
    sku_code = Column(String, unique=True, nullable=False)
    unit_cost = Column(Float, nullable=False)
    mrp = Column(Float, nullable=False)

    shade = relationship("Shade", back_populates="skus")
