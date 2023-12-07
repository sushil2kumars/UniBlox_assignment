from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Coupon, User, OrderProduct, Order
from app import get_db, get_current_user
from sqlalchemy_utils import UUIDType
from pydantic import BaseModel
from uuid import UUID
from sqlalchemy import func
from sqlalchemy.sql import exists

router = APIRouter()

class CreateCoupon(BaseModel):
    code: str
    nth_order: float
    discount_percent: float

# Read all coupons
@router.get("/coupons/")
def read_coupons(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve all coupons. Only accessible to admin users.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can access coupons")

    db_coupons = db.query(Coupon).all()
    if not db_coupons:
        raise HTTPException(status_code=404, detail="Coupons not found")
    
    return db_coupons

# Create a new coupon
@router.post("/coupons/")
def create_coupon(coupon: CreateCoupon, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Create a new coupon. Only accessible to admin users.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can create coupons")
    
    db_coupon = Coupon(**coupon.dict())
    db.add(db_coupon)
    db.commit()
    db.refresh(db_coupon)
    return db_coupon

# Read a specific coupon by code
@router.get("/coupons/{coupon_code}")
def read_coupon(coupon_code: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve a specific coupon by code. Only accessible to admin users.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can access coupons")

    db_coupon = db.query(Coupon).filter(Coupon.code == coupon_code).first()
    if not db_coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    return db_coupon

# Delete a coupon by ID
@router.delete("/coupons/{coupon_id}")
def delete_coupon(coupon_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Delete a coupon by ID. Only accessible to admin users.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can delete coupons")

    db_coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not db_coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    db.delete(db_coupon)
    db.commit()
    return db_coupon

# Get purchase statistics
@router.get("/purchase_statistics")
@router.get("/purchase_statistics")
def purchase_statistics(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve purchase statistics. Only accessible to admin users.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can access purchase statistics")

    discount_codes_ = db.query(OrderProduct).all()
    print(discount_codes_,"dd")
    total_items_purchased = db.query(func.coalesce(func.sum(OrderProduct.quantity), 0)).scalar()
    total_purchase_amount = db.query(func.coalesce(func.sum(Order.total_amount), 0.0)).scalar()
    discount_codes = db.query(Coupon.code).all()
    total_discount_amount = sum(order.total_amount * 0.1 for order in db.query(Order).filter(Order.discount_code.isnot(None)).all())

    return {
        "total_items_purchased": total_items_purchased,
        "total_purchase_amount": total_purchase_amount,
        "discount_codes": [code for code, in discount_codes],
        "total_discount_amount": total_discount_amount,
    }