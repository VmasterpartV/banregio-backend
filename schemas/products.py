from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class Category(BaseModel):
    name: str
    description: Optional[str] = None
    min_units: Optional[int] = None
    get_units: Optional[int] = None
    created_date: datetime = datetime.now()

class ListCategories(BaseModel):
    predictions: List[Category]

class Product(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    buy_price: Optional[float] = None
    sell_price: Optional[float] = None
    stock: Optional[int] = None
    created_date: datetime = datetime.now()

class ListProducts(BaseModel):
    products: List[Product]

class SellProduct(BaseModel):
    product_id: int
    units: int
    price: float
    created_date: datetime = datetime.now()

class Sell(BaseModel):
    sell_products: str
    total: Optional[float] = None
    client: Optional[str] = None
    created_date: datetime = datetime.now()

class ListSells(BaseModel):
    sells: List[Sell]
        