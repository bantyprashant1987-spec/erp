from uuid import UUID
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime, date
from typing import List


class SaleItemCreate(BaseModel):
    product_id: UUID
    quantity: int = Field(..., ge=1)
    unit_price: Decimal


class SaleCreate(BaseModel):
    shop_id: UUID
    discount: Decimal = Field(default=0, ge=0)
    payment_mode: str
    gst_percentage: Decimal = Field(default=0, ge=0)
    items: List[SaleItemCreate]


class SaleItemRead(BaseModel):
    id: UUID
    product_id: UUID
    quantity: int
    unit_price: Decimal
    line_total: Decimal

    class Config:
        from_attributes = True


class SaleRead(BaseModel):
    id: UUID
    shop_id: UUID
    user_id: UUID | None
    total_amount: Decimal
    discount: Decimal
    payment_mode: str
    gst_amount: Decimal
    created_at: datetime
    items: List[SaleItemRead]

    class Config:
        from_attributes = True


class DailySalesReport(BaseModel):
    date: date
    total_sales: Decimal
    total_discount: Decimal
    total_gst: Decimal
    total_orders: int
