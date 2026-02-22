from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import authenticate_user, get_current_active_user, get_db_dep, get_owner_user
from app.core.security import create_access_token, get_password_hash
from app.models import User, UserRole
from app.schemas.auth import LoginRequest, Token, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(login_req: LoginRequest, db: Session = Depends(get_db_dep)):
    user = authenticate_user(db, login_req.email, login_req.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(str(user.id))
    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/staff", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_staff(
    staff_in: UserCreate,
    db: Session = Depends(get_db_dep),
    owner: User = Depends(get_owner_user),
):
    if db.query(User).filter(User.email == staff_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    staff = User(
        email=staff_in.email,
        hashed_password=get_password_hash(staff_in.password),
        role=UserRole.STAFF,
        shop_id=owner.shop_id,
        is_active=True,
    )
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff
