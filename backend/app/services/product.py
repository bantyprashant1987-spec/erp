from uuid import uuid4, UUID
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Product
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(db: Session, product_in: ProductCreate) -> Product:
    product = Product(
        id=uuid4(),
        name=product_in.name,
        category=product_in.category,
        purchase_price=product_in.purchase_price,
        selling_price=product_in.selling_price,
        stock_quantity=product_in.stock_quantity,
        low_stock_threshold=product_in.low_stock_threshold,
        shop_id=product_in.shop_id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product_id: UUID, product_in: ProductUpdate, shop_id: UUID) -> Product:
    product = db.query(Product).filter(Product.id == product_id, Product.shop_id == shop_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for field, value in product_in.model_dump(exclude_unset=True).items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: UUID, shop_id: UUID) -> None:
    product = db.query(Product).filter(Product.id == product_id, Product.shop_id == shop_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()


def list_products(db: Session, shop_id: UUID) -> List[Product]:
    return db.query(Product).filter(Product.shop_id == shop_id).order_by(Product.name).all()
