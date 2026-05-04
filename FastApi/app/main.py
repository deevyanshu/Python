from fastapi import FastAPI,HTTPException, Query, Path
from app.services.products import get_all_products, add_product, remove_product, change_product
from app.schema.product import Product,ProductUpdate
from uuid import uuid4, UUID
from datetime import datetime
from typing import List,Dict

app=FastAPI()

@app.get('/')
def root():
    return {"message":"Hello World"}


# @app.get('/products')
# def get_products():
#     return get_all_products()

#filtering by name
# @app.get('/products')
# def list_products(name:str=Query(None, min_length=3, max_length=50,description="Search by product name(case insensitive)")):

#     products=get_all_products()
#     if name:
#         needle=name.strip().lower()
#         products=[p for p in products if needle in p.get("name","").lower()]
#         if not products:
#             raise HTTPException(status_code=404, detail=f"No products found matching '{name}'")
        
#         total=len(products)
    
#     return{"total":total,
#         "products":products}

#sort by price
# @app.get('/products')
# def list_products(name:str=Query(None, min_length=3, max_length=50,description="Search by product name(case insensitive)"),sort_by_price:bool=Query(default=False, description="Sort products by price"),order:str=Query(default="asc", description="Sort order when sort_by_price=true (asc,desc)")):

#     products=get_all_products()
#     if name:
#         needle=name.strip().lower()
#         products=[p for p in products if needle in p.get("name","").lower()]
#     if not products:
#         raise HTTPException(status_code=404, detail=f"No products found matching '{name}'")
    
#     if sort_by_price:
#         reverse =order =="desc" #True for descending order, False for ascending order
#         products=sorted(products,key=lambda p:p.get("price",0),reverse=reverse)
        
#     total=len(products)
    
#     return{"total":total,
#         "products":products}

#limit and pagination
@app.get('/products',response_model=Dict)
def list_products(name:str=Query(None, min_length=3, max_length=50,description="Search by product name(case insensitive)"),sort_by_price:bool=Query(default=False, description="Sort products by price"),order:str=Query(default="asc", description="Sort order when sort_by_price=true (asc,desc)"),limit:int=Query(default=5,ge=1,le=100,description="Number of items"),offset:int=Query(default=0,ge=0,description="Pagination offset")):

    products=get_all_products()
    if name:
        needle=name.strip().lower()
        products=[p for p in products if needle in p.get("name","").lower()]
    if not products:
        raise HTTPException(status_code=404, detail=f"No products found matching '{name}'")
    
    if sort_by_price:
        reverse =order =="desc" #True for descending order, False for ascending order
        products=sorted(products,key=lambda p:p.get("price",0),reverse=reverse)
        
    products=products[offset:offset+limit]
    total=len(products)
    return{"total":total,
        "products":products}

#get product by id
@app.get('/products/{product_id}',response_model=Dict)
def get_product_by_id(product_id:str=Path(...,min_length=36, max_length=36, description="The ID of the product to retrieve")):
    products=get_all_products()
    for product in products:
        if product["id"]==product_id:
            return product
    raise HTTPException(status_code=404, detail=f"Product with id '{product_id}' not found")


#post api
@app.post("products",status_code=201)
def create_product(product:Product):
    product_dict=product.model_dump(mode="json")
    product_dict["id"]=str(uuid4())
    product_dict["created_at"]=datetime.utcnow().isoformat()+"Z"
    try:
        add_product(product_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
 
 #delete api
@app.delete("/products/{product_id}")
def delete_product(product_id: UUID=Path(..., description="The ID of the product to delete")):
        try:
            data=remove_product(str(product_id))
            return data
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e)) 

@app.put("/products/{product_id}")
def update_product(product_id:UUID=Path(..., description="The ID of the product to update"), payload: ProductUpdate=None):
    try:
        update_product=change_product(str(product_id),payload.model_dump(mode="json",exclude_unset=True))
        return update_product
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
