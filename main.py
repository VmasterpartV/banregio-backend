from fastapi import FastAPI, status
from config.database import Session, engine, Base
from models.products import ProductModel, CategoryModel, SellModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.products import ListProducts, Product, Category, Sell, ListSells, SellProduct
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
import json

app = FastAPI(title="Backend Api", description="API for products system", version="0.1.0")

Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()

@app.get("/products/", status_code=status.HTTP_200_OK, response_model=ListProducts, summary="Get all products", tags=["Products"])
def get_products():
    """
    Get all products
    
    Returns a list of products.
    """
    db = Session()
    products = db.query(ProductModel).all()
    db.close()

    # Retornar nombre de categoria
    for product in products:
        print(product.category_id)
        if product.category_id is not None:
            category = db.query(CategoryModel).filter(CategoryModel.id == product.category_id).first()
            print(category)
            product.category_id = category.name
            print(product.category_id)

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(products))

@app.post("/products/", status_code=status.HTTP_201_CREATED, response_model=None, summary="Create a product", tags=["Products"])
def create_product(data: Product):
    """
    Create a product
    
    Returns the created product.
    """
    print(data.name)
    db = Session()
    product = ProductModel(name=data.name, description=data.description, category_id=data.category_id, buy_price=data.buy_price, sell_price=data.sell_price, stock=data.stock)
    db.add(product)
    db.commit()
    db.refresh(product)
    db.close()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(product))

@app.get("/categories/", status_code=status.HTTP_200_OK, response_model=ListProducts, summary="Get all categories", tags=["Categories"])
def get_categories():
    """
    Get all categories
    
    Returns a list of categories.
    """
    db = Session()
    categories = db.query(CategoryModel).all()
    db.close()
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(categories))

@app.post("/categories/", status_code=status.HTTP_201_CREATED, response_model=None, summary="Create a category", tags=["Categories"])
def create_category(data: Category):
    """
    Create a category
    
    Returns the created category.
    """
    db = Session()
    category = CategoryModel(name=data.name, description=data.description, min_units=data.min_units, get_units=data.get_units)
    db.add(category)
    db.commit()
    db.refresh(category)
    db.close()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(category))

@app.get("/sells/", status_code=status.HTTP_200_OK, response_model=ListSells, summary="Get all sells", tags=["Sells"])
def get_sells():
    """
    Get all sells
    
    Returns a list of sells.
    """
    db = Session()
    sells = db.query(SellModel).all()

    db.close()
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(sells))

@app.post("/sells/", status_code=status.HTTP_201_CREATED, response_model=None, summary="Create a sell", tags=["Sells"])
def create_sell(data: Sell):
    """
    Create a sell
    
    Returns the created sell.
    """
    db = Session()
    # Crear SellProduct para cada producto
    sell_products = []
    total = 0
    # str to array, ejemplo de str "[{'product_id':1, 'units':2},{'product_id':2, 'units':3}]"
    original_data = data.sell_products
    data.sell_products = json.loads(data.sell_products.replace("'", "\""))

    for product in data.sell_products:
        product = jsonable_encoder(product)
        product_db = db.query(ProductModel).filter(ProductModel.id == product['product_id']).first()
        product_db.stock = product_db.stock - product['units']
        db.commit()
        db.refresh(product_db)
        price = product_db.sell_price * product['units']
        sell_product = SellProduct(product_id=product['product_id'], units=product['units'], price=price)
        sell_products.append(sell_product)
        total += price * product['units']
    # Crear Sell
    sell = SellModel(sell_products=jsonable_encoder(original_data), total=total, client=data.client)
    db.add(sell)
    db.commit()
    db.refresh(sell)
    db.close()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(sell))

@app.post("/stock/", status_code=status.HTTP_201_CREATED, response_model=None, summary="Add stock", tags=["Stock"])
def add_stock():
    """
    Add stock
    
    Check if the product have the category min_units and add the category get_units to the product stock.
    """
    db = Session()
    products = db.query(ProductModel).all()
    updated_products = []
    for product in products:
        if product.category_id is not None:
            category = db.query(CategoryModel).filter(CategoryModel.id == product.category_id).first()
            if product.stock <= category.min_units:
                product.stock += category.get_units
                db.commit()
                db.refresh(product)
                updated_products.append(product)
    db.close()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(updated_products))
