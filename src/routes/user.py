from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.user import get_all_users
from security.oauth import get_current_user
from schemas.user import UserResponse, UserCreate
from config.database import Base, engine, SessionLocal


router = APIRouter()


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/')
def read_root():
    return 'Server is running..'


@router.get('/users', response_model=list[UserResponse])
def users(db: Session= Depends(get_db)):
    users = get_all_users(db)
    return users


# @router.post("/password-recovery/{email}", response_model=schemas.Msg)
# def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
#     """
#     Password Recovery
#     """
#     user = crud.user.get_by_email(db, email=email)

#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system.",
#         )
#     password_reset_token = generate_password_reset_token(email=email)
#     send_reset_password_email(
#         email_to=user.email, email=email, token=password_reset_token
#     )
#     return {"msg": "Password recovery email sent"}