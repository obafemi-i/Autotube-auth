from sqlalchemy.orm import Session

from schemas.user import UserResponse, UserCreate
from models.user import User
from security. hashing import get_password_hash



def create_user(db: Session, obj_in: UserCreate) -> UserResponse:
    db_obj = User(
        email=obj_in.email,
        hashed_password=get_password_hash(obj_in.password),
        # first_name=obj_in.first_name
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj



def get_by_email(db: Session, email: str) -> UserResponse | None:
    user = db.query(User).filter(User.email == email).first()
    return user


def get_all_users(db: Session) -> list[UserResponse]:
    users = db.query(User).all()
    return users


def get_by_id(id: int, db: Session) -> UserResponse:
    user = db.query(User).filter(User.id == id).first()
    return user
