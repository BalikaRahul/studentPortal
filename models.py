from database import Base
from sqlalchemy import Column,String,Integer

class RegisterForm(Base):
    __tablename__="RegisterForm"
    id=Column(Integer,primary_key=True,autoincrement=True)
    first_name= Column(String,nullable=False)
    last_name= Column(String,nullable=True)
    phone_number= Column(String,nullable=True)
    email= Column(String,nullable=False,unique=True)
    gender= Column(String,nullable=True)
    city=Column(String,nullable=False)
    role= Column(String,nullable=True)
    password = Column(String,nullable=False)