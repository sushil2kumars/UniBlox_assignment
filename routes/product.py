from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Product, User
from app import get_db, get_current_user

router = APIRouter()

@router.get("/")
def get_product_list(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products


@router.post("/")
def add_product(product_data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_product = Product(**product_data)
    if current_user.is_admin:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product

    else:
        return  HTTPException(status_code=403, detail="Only admin can update product")
    
@router.put("/{product_id}")
def update_product(product_id: str, product_data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can update product")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product  

@router.delete("/{product_id}", response_model=dict)
def delete_product(product_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can delete product")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}