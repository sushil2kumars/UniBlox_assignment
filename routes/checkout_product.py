
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Product, User, Cart, Order, OrderProduct, Coupon, CartProduct
from app import get_db, get_current_user
from sqlalchemy import select

router = APIRouter()


@router.post("/checkout")
def checkout(discount_code: str = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get items from the user's cart
    cart_items = db.query(CartProduct).join(Cart).filter(Cart.user_id == str(current_user.id)).all()
  
    if not cart_items:
        raise HTTPException(status_code=400, detail="No items in the cart")

    # Calculate total amount
    total_amount = sum(db.query(Product).filter(Product.id == product.product_id).first().price*product.quantity for product in cart_items)
    #sum(item.product.price * item.quantity for item in produc_list)
    print(total_amount,"amount")
    # Apply discount if the discount code is valid
    discount_percent = 0.0
    if discount_code:
        coupon = db.query(Coupon).filter(Coupon.code == discount_code).first()

        # fetch last order id and get current id for applying coopen code
        last_pk = db.execute(select(Order.id).order_by(Order.id.desc()).limit(1)).scalar()
        current_order_number = last_pk+1 if last_pk else 1 

        if coupon and current_order_number % coupon.nth_order == 0:
            discount_percent = coupon.discount_percent

        elif coupon:
            raise HTTPException(status_code=400, detail="Invalid coupon code")


    # Create an order
    new_order = Order(user_id=current_user.id, total_amount=total_amount, paid_amount=total_amount * (1 - discount_percent / 100.0), discount_code=discount_code)
    db.add(new_order)
    db.commit()

    # Move cart items to ProductOrder
    for item in cart_items:
        product_order = OrderProduct(order_id=new_order.id, product_id=item.product_id, quantity=item.quantity)
        db.add(product_order)
    
    db.commit()
    
    #db.delete(cart_items)
    delete_query = db.query(CartProduct).filter(CartProduct.cart_id == str(cart_items[0].cart_id))

    delete_query.delete()
 
    db.commit()
  
    # Clear the user's cart
    print(db.query(Cart).filter(Cart.user_id == current_user.id).delete())
    #cart_items.delete()
    db.commit()

    return {"message": "Checkout successful", "total_amount": new_order.total_amount}
