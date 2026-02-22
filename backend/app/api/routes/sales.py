from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db_dep, ensure_same_shop
from app.models import User
from app.schemas.sale import SaleCreate, SaleRead
from app.services import sale as sale_service

router = APIRouter(prefix="/sales", tags=["sales"])


@router.post("/", response_model=SaleRead, status_code=status.HTTP_201_CREATED)
def create_sale(
    sale_in: SaleCreate,
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_active_user),
):
    ensure_same_shop(sale_in.shop_id, current_user)
    enforced_sale = SaleCreate(
        **sale_in.model_dump(exclude={"shop_id"}),
        shop_id=current_user.shop_id,
    )
    sale = sale_service.create_sale(db, enforced_sale, current_user.id)
    return sale
