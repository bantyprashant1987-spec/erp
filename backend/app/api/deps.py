from typing import Generator
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import verify_password
from app.db.session import get_db
from app.models import User, UserRole
from app.schemas.auth import TokenData

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_db_dep() -> Generator:
    yield from get_db()


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_current_user(
    db: Session = Depends(get_db_dep), token: str = Depends(reuseable_oauth)
) -> User:
    settings = get_settings()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        sub: str | None = payload.get("sub")
        if sub is None:
            raise credentials_exception
        token_data = TokenData(sub=sub)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == UUID(token_data.sub)).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_owner_user(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role != UserRole.OWNER:
        raise HTTPException(status_code=403, detail="Owner access required")
    return current_user


def ensure_same_shop(shop_id: UUID, user: User) -> None:
    if user.shop_id != shop_id:
        raise HTTPException(status_code=403, detail="Cross-shop access denied")
