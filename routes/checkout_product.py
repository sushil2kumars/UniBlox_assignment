
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Product, User, Cart, Order, OrderProduct, Coupon
from app import get_db, get_current_user

router = APIRouter()


@router.post("/checkout")
def checkout(cart_id: str, discount_code: str = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get items from the user's cart
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id, Cart.id == cart_id).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="No items in the cart")

    # Calculate total amount
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    # Apply discount if the discount code is valid
    discount_percent = 0.0
    if discount_code:
        coupon = db.query(Coupon).filter(Coupon.code == discount_code).first()
        if coupon:
            discount_percent = coupon.discount_percent
        else:
            raise HTTPException(status_code=400, detail="Invalid coupon code")


    # Create an order
    new_order = Order(user_id=current_user.id, total_amount=total_amount * (1 - discount_percent / 100.0), discount_code=discount_code)
    db.add(new_order)
    db.commit()

    # Move cart items to ProductOrder
    for item in cart_items:
        product_order = OrderProduct(order_id=new_order.id, product_id=item.product_id, quantity=item.quantity)
        db.add(product_order)

    # Clear the user's cart
    db.query(Cart).filter(Cart.user_id == current_user.id).delete()
    db.commit()

    return {"message": "Checkout successful", "total_amount": new_order.total_amount}