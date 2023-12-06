from config.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String, nullable=True)
    min_units = Column(Integer, nullable=True)
    get_units = Column(Integer, nullable=True)
    created_date = Column(DateTime, default=datetime.now)

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String, nullable=True)
    category_id = Column(Integer, nullable=True)
    buy_price = Column(Float, nullable=True)
    sell_price = Column(Float, nullable=True)
    stock = Column(Integer, nullable=True)
    created_date = Column(DateTime, default=datetime.now)

class SellModel(Base):
    __tablename__ = "sells"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sell_products = Column(String)
    total = Column(Float)
    client = Column(String)
    created_date = Column(DateTime, default=datetime.now)
