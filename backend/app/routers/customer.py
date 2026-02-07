from __future__ import annotations
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Shade, SKU, Product, Dealer, InventoryLevel, CustomerOrderRequest
from datetime import datetime
import math

router = APIRouter()


class OrderRequestCreate(BaseModel):
    customer_name: str
    customer_phone: str
    shade_id: int
    size_preference: str = "4L"
    dealer_id: int


@router.get("/shades")
def get_shades(
    family: str = None, category: str = None, trending: bool = None,
    db: Session = Depends(get_db),
):
    query = db.query(Shade)
    if family:
        query = query.filter(Shade.shade_family == family)
    if trending is not None:
        query = query.filter(Shade.is_trending == trending)

    shades = query.all()
    result = []
    for s in shades:
        product = db.query(Product).filter(Product.id == s.product_id).first()
        if category and product and product.category != category:
            continue
        result.append({
            "id": s.id,
            "shade_code": s.shade_code,
            "shade_name": s.shade_name,
            "hex_color": s.hex_color,
            "shade_family": s.shade_family,
            "is_trending": s.is_trending,
            "product_name": product.name if product else "",
            "product_category": product.category if product else "",
            "finish": product.finish if product else "",
        })
    return result


@router.get("/shades/{shade_id}")
def get_shade_detail(shade_id: int, db: Session = Depends(get_db)):
    shade = db.query(Shade).filter(Shade.id == shade_id).first()
    if not shade:
        return {"error": "Shade not found"}

    product = db.query(Product).filter(Product.id == shade.product_id).first()
    skus = db.query(SKU).filter(SKU.shade_id == shade.id).all()

    return {
        "id": shade.id,
        "shade_code": shade.shade_code,
        "shade_name": shade.shade_name,
        "hex_color": shade.hex_color,
        "rgb": {"r": shade.rgb_r, "g": shade.rgb_g, "b": shade.rgb_b},
        "shade_family": shade.shade_family,
        "is_trending": shade.is_trending,
        "product": {
            "name": product.name if product else "",
            "category": product.category if product else "",
            "finish": product.finish if product else "",
            "base_type": product.base_type if product else "",
        },
        "sizes": [
            {"size": sku.size, "sku_code": sku.sku_code, "mrp": sku.mrp, "sku_id": sku.id}
            for sku in sorted(skus, key=lambda x: float(x.size.replace("L", "")))
        ],
    }


@router.get("/shades/{shade_id}/availability")
def shade_availability(shade_id: int, lat: float = 19.07, lng: float = 72.87, db: Session = Depends(get_db)):
    """Find nearby dealers with stock for this shade."""
    shade = db.query(Shade).filter(Shade.id == shade_id).first()
    if not shade:
        return []

    # Get 4L SKU for this shade
    sku = db.query(SKU).filter(SKU.shade_id == shade_id, SKU.size == "4L").first()
    if not sku:
        return []

    dealers = db.query(Dealer).all()
    results = []

    for dealer in dealers:
        # Calculate distance
        dist = _haversine(lat, lng, dealer.latitude, dealer.longitude)
        if dist > 50:  # 50km radius
            continue

        # Check stock at dealer's warehouse
        level = db.query(InventoryLevel).filter(
            InventoryLevel.warehouse_id == dealer.warehouse_id,
            InventoryLevel.sku_id == sku.id,
        ).first()

        stock = level.current_stock if level else 0
        if stock > 50:
            stock_status = "In Stock"
        elif stock > 0:
            stock_status = "Low Stock"
        else:
            stock_status = "Out of Stock"

        results.append({
            "dealer_id": dealer.id,
            "dealer_name": dealer.name,
            "city": dealer.city,
            "distance_km": round(dist, 1),
            "stock_status": stock_status,
            "stock_qty": stock,
            "latitude": dealer.latitude,
            "longitude": dealer.longitude,
        })

    return sorted(results, key=lambda x: x["distance_km"])[:10]


@router.get("/dealers/nearby")
def nearby_dealers(lat: float = 19.07, lng: float = 72.87, db: Session = Depends(get_db)):
    dealers = db.query(Dealer).all()
    results = []
    for d in dealers:
        dist = _haversine(lat, lng, d.latitude, d.longitude)
        if dist < 50:
            results.append({
                "id": d.id,
                "name": d.name,
                "city": d.city,
                "distance_km": round(dist, 1),
                "tier": d.tier,
                "latitude": d.latitude,
                "longitude": d.longitude,
            })
    return sorted(results, key=lambda x: x["distance_km"])[:10]


@router.post("/order-request")
def create_order_request(req: OrderRequestCreate, db: Session = Depends(get_db)):
    order_req = CustomerOrderRequest(
        customer_name=req.customer_name,
        customer_phone=req.customer_phone,
        shade_id=req.shade_id,
        size_preference=req.size_preference,
        dealer_id=req.dealer_id,
        status="requested",
        created_at=datetime.utcnow(),
    )
    db.add(order_req)
    db.commit()
    return {"success": True, "request_id": order_req.id, "status": "requested"}


@router.post("/snap-find")
async def snap_and_find(hex_color: str = "#FFD700", db: Session = Depends(get_db)):
    """
    Find closest shade match for a given hex color.
    In production with Gemini Vision, this would accept an image upload.
    """
    # Parse input hex
    target_r, target_g, target_b = _hex_to_rgb(hex_color)

    # Find closest shade by Euclidean RGB distance
    shades = db.query(Shade).all()
    best_match = None
    best_distance = float("inf")

    for shade in shades:
        dist = math.sqrt(
            (shade.rgb_r - target_r) ** 2 +
            (shade.rgb_g - target_g) ** 2 +
            (shade.rgb_b - target_b) ** 2
        )
        if dist < best_distance:
            best_distance = dist
            best_match = shade

    if not best_match:
        return {"error": "No match found"}

    product = db.query(Product).filter(Product.id == best_match.product_id).first()

    return {
        "detected_color": {"hex": hex_color, "rgb": {"r": target_r, "g": target_g, "b": target_b}},
        "match": {
            "shade_name": best_match.shade_name,
            "shade_code": best_match.shade_code,
            "hex_color": best_match.hex_color,
            "shade_family": best_match.shade_family,
            "product_name": product.name if product else "",
            "confidence": round(max(0, 100 - best_distance / 4.41), 1),
        },
        "shade_id": best_match.id,
    }


def _haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _hex_to_rgb(hex_color: str):
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
