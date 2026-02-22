from uuid import UUID
from pydantic import BaseModel


class ShopBase(BaseModel):
    name: str
    gst_number: str | None = None


class ShopCreate(ShopBase):
    pass


class ShopRead(ShopBase):
    id: UUID

    class Config:
        from_attributes = True
