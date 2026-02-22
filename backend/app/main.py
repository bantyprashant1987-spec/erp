import uuid
from decimal import Decimal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.api.routes import auth, products, sales, reports
from app.core.config import get_settings
from app.db.base import Base  # noqa: F401
from app.db.session import engine, SessionLocal
from app.schemas.shop import ShopCreate
from app.schemas.auth import UserCreate
from app.services.auth import init_owner
from app.models import Product


settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.cors_origins] if settings.cors_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(sales.router, prefix="/api")
app.include_router(reports.router, prefix="/api")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        owner = init_owner(
            db,
            ShopCreate(name="Default Shop", gst_number=None),
            UserCreate(
                email=settings.admin_email,
                password=settings.admin_password,
                role="owner",
                shop_id=None,  # type: ignore[arg-type]
            ),
        )
        seed_products(db, owner.shop_id)
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "ok"}


def seed_products(db: Session, shop_id) -> None:
    existing = db.query(Product).filter(Product.shop_id == shop_id).count()
    if existing > 0:
        return

    sample = [
        ("Paracetamol 500mg", "Medicine", Decimal("1.50"), Decimal("3.00"), 120, 10),
        ("Ibuprofen 400mg", "Medicine", Decimal("2.00"), Decimal("4.50"), 90, 10),
        ("Cetirizine 10mg", "Medicine", Decimal("1.00"), Decimal("2.50"), 150, 15),
        ("Amoxicillin 500mg", "Antibiotic", Decimal("4.00"), Decimal("8.50"), 60, 8),
        ("ORS Sachet", "Rehydration", Decimal("0.60"), Decimal("1.20"), 200, 20),
    ]

    for name, category, purchase_price, selling_price, stock, low_stock in sample:
        db.add(
            Product(
                id=uuid.uuid4(),
                name=name,
                category=category,
                purchase_price=purchase_price,
                selling_price=selling_price,
                stock_quantity=stock,
                low_stock_threshold=low_stock,
                shop_id=shop_id,
            )
        )

    db.commit()
