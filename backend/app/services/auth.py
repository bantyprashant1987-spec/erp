from uuid import uuid4
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core.security import get_password_hash
from app.models import User, Shop, UserRole
from app.schemas.auth import UserCreate
from app.schemas.shop import ShopCreate


def init_owner(db: Session, shop_in: ShopCreate, user_in: UserCreate) -> User:
    existing_owner = db.query(User).filter(User.email == user_in.email).first()
    if existing_owner:
        return existing_owner

    shop = Shop(id=uuid4(), name=shop_in.name, gst_number=shop_in.gst_number)
    db.add(shop)
    db.flush()

    owner = User(
        id=uuid4(),
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=UserRole.OWNER,
        shop_id=shop.id,
        is_active=True,
    )
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return owner
