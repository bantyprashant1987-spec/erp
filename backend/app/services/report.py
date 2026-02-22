from datetime import date, datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import Sale
from app.schemas.sale import DailySalesReport


def daily_sales_report(db: Session, shop_id, report_date: date | None = None) -> DailySalesReport:
    target_date = report_date or date.today()
    start_dt = datetime.combine(target_date, datetime.min.time())
    end_dt = datetime.combine(target_date, datetime.max.time())

    totals = (
        db.query(
            func.coalesce(func.sum(Sale.total_amount), 0),
            func.coalesce(func.sum(Sale.discount), 0),
            func.coalesce(func.sum(Sale.gst_amount), 0),
            func.count(Sale.id),
        )
        .filter(Sale.shop_id == shop_id)
        .filter(Sale.created_at >= start_dt)
        .filter(Sale.created_at <= end_dt)
        .one()
    )

    total_sales, total_discount, total_gst, total_orders = totals

    return DailySalesReport(
        date=target_date,
        total_sales=Decimal(total_sales),
        total_discount=Decimal(total_discount),
        total_gst=Decimal(total_gst),
        total_orders=total_orders,
    )
