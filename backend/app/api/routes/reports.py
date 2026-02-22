from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db_dep
from app.models import User
from app.schemas.sale import DailySalesReport
from app.services.report import daily_sales_report

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/daily", response_model=DailySalesReport)
def get_daily_report(
    report_date: date | None = None,
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_active_user),
):
    return daily_sales_report(db, current_user.shop_id, report_date)
