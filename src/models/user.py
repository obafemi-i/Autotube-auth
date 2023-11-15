from sqlalchemy import Integer, String, Column
from config.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(30), unique=True, index=True)
    password = Column(String(150))
    first_name = Column(String(50), index=True)
    account = Column(String(40))

