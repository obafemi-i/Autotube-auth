from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from crud.user import get_all_users, create_user, get_by_id, get_by_email
from security.oauth import get_current_user
from security.hashing import verify_password
from security.tokens import create_access_token
from schemas.user import UserResponse, UserCreate
from config.database import Base, engine, SessionLocal
from models.user import User


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
def all_users(db: Session= Depends(get_db), current_user: UserCreate = Depends(get_current_user)):
    users = get_all_users(db)
    return users



@router.get('/user/{email}', response_model=UserResponse)
def by_email(email: str, db: Session = Depends(get_db)):
    user = get_by_email(email=email, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'No user with email {email}')
    return user



@router.post('/create', response_model=UserResponse)
def create(request: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, obj_in=request)
    return user



@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid login details')
    
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid login derails')
    
    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}



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