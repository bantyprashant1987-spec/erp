from uuid import uuid4, UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Sale, SaleItem, Product
from app.schemas.sale import SaleCreate


def create_sale(db: Session, sale_in: SaleCreate, user_id: UUID | None) -> Sale:
    products = (
        db.query(Product)
        .filter(Product.id.in_([item.product_id for item in sale_in.items]), Product.shop_id == sale_in.shop_id)
        .all()
    )
    product_map = {p.id: p for p in products}

    # Validate stock
    for item in sale_in.items:
        product = product_map.get(item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")

    gst_amount = Decimal("0")
    sub_total = Decimal("0")

    for item in sale_in.items:
        line_total = item.unit_price * item.quantity
        sub_total += line_total
        if sale_in.gst_percentage:
            gst_amount += (line_total * sale_in.gst_percentage) / Decimal("100")

    total_amount = sub_total + gst_amount - sale_in.discount

    sale = Sale(
        id=uuid4(),
        shop_id=sale_in.shop_id,
        user_id=user_id,
        discount=sale_in.discount,
        payment_mode=sale_in.payment_mode,
        gst_amount=gst_amount,
        total_amount=total_amount,
    )
    db.add(sale)
    db.flush()

    for item in sale_in.items:
        line_total = item.unit_price * item.quantity
        sale_item = SaleItem(
            id=uuid4(),
            sale_id=sale.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            line_total=line_total,
        )
        db.add(sale_item)

        product = product_map[item.product_id]
        product.stock_quantity -= item.quantity

    db.commit()
    db.refresh(sale)
    return sale
