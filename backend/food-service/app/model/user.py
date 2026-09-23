from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship
from app.model.food import FoodItemModel

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)    
    hashed_password = Column(String, nullable=True)
    food_items = relationship("FoodItemModel", back_populates="owner", cascade="all, delete-orphan")