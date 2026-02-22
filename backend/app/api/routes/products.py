from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db_dep, ensure_same_shop
from app.models import User
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services import product as product_service

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[ProductRead])
def list_products(
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_active_user),
):
    return product_service.list_products(db, current_user.shop_id)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_active_user),
):
    ensure_same_shop(product_in.shop_id, current_user)
    enforced_payload = ProductCreate(**product_in.model_dump(), shop_id=current_user.shop_id)
    return product_service.create_product(db, enforced_payload)


@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: UUID,
    product_in: ProductUpdate,
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_active_user),
):
    return product_service.update_product(db, product_id, product_in, current_user.shop_id)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: UUID,
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_active_user),
):
    product_service.delete_product(db, product_id, current_user.shop_id)
    return None
