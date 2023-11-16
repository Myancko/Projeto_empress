import datetime
import security
from pydantic import validator, field_validator
from sqlalchemy import ForeignKey, Date, Column, String, Integer, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User (Base):  
    
    __tablename__ = "user"
    
    id_user = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)
    matricula = Column(Integer, unique=True, nullable=True) 
    email = Column(String, unique=True, nullable=True)
    number = Column(String, nullable=True)
    role = Column(Integer, nullable=True)
    
    @field_validator('password')
    def hash_password(cls, v):
        return security.get_password_hash(v)
    
class Request (Base):

    __tablename__ = "request"

    id_request = Column(Integer, primary_key=True, index=True)
    data = Column(String)
    color = Column(Boolean)
    two_sided = Column(Boolean)
    quantity = Column(Integer)
    status = Column(String)
    date = Column(Date)
    owner = Column(Integer, ForeignKey('user.id_user'))