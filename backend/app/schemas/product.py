from uuid import UUID
from pydantic import BaseModel, Field
from decimal import Decimal


class ProductBase(BaseModel):
    name: str
    category: str | None = None
    purchase_price: Decimal = Field(default=0)
    selling_price: Decimal = Field(default=0)
    stock_quantity: int = Field(default=0, ge=0)
    low_stock_threshold: int = Field(default=5, ge=0)


class ProductCreate(ProductBase):
    shop_id: UUID


class ProductUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    purchase_price: Decimal | None = None
    selling_price: Decimal | None = None
    stock_quantity: int | None = Field(default=None, ge=0)
    low_stock_threshold: int | None = Field(default=None, ge=0)


class ProductRead(ProductBase):
    id: UUID
    shop_id: UUID

    class Config:
        from_attributes = True
