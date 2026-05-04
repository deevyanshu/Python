import json
from pathlib import Path
from typing import List,Dict

DATA_FILE=Path(__file__).parent.parent / 'data' / 'products.json'

def load_products() -> List[Dict]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE,'r',encoding="utf-8") as file:
        return json.load(file)

def get_all_products() -> List[Dict]:
    return load_products()

def save_product(products:List[Dict])-> None:
    with open(DATA_FILE,"w",encoding="utf-8") as file:
        json.dump(products,file,indent=2,ensure_ascii=False)

def add_product(product:Dict) -> Dict:
    products=get_all_products()
    if any(p["sku"]==product["sku"] for p in products):
        raise ValueError(f"Product with SKU '{product['sku']}' already exists")
    products.append(product)
    save_product(products)
    return product

def remove_product(id:str) -> str:
    products=get_all_products()

    for idx,p in enumerate(products):
        if p["id"]==str(id):
            deleted=products.pop(idx)
            save_product(products)
            return {"message":f"Product with id '{id}' deleted successfully",
                    "product":deleted
                    }

def change_product(product_id:str,update_data:dict):
    products=get_all_products()
    for idx,p in enumerate(products):
        if p["id"]==product_id:
            for key,value in update_data.item():
                if value is None:
                    continue

                if isinstance(value,dict) and isinstance(p.get(key),dict):
                    p[key].update(value)
                else:
                    p[key]=value
            products[idx]=p
            save_product(products)
            return p
    raise ValueError(f"Product with id '{product_id}' not found")