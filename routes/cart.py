from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Cart, CartProduct, User,Product
from app import get_db, get_current_user

router = APIRouter()


@router.get("/")
def get_cart_products(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Get cart products from the database
    products = db.query(CartProduct).join(Cart).filter(Cart.user_id == str(current_user.id)).all()
    
    # Get product details and return the data
    return [{"details":db.query(Product).filter(Product.id == product.product_id).first(),"order":product} for product in products]


@router.post("/")
def add_to_cart(product_id: str, quantity: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check for existing cart
    cart = db.query(Cart).filter(Cart.user_id == str(current_user.id)).first()

    # If cart doesn't exist, create a new one
    if not cart:
        cart = Cart(user_id=str(current_user.id))
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Check for existing cart product
    cart_product = db.query(CartProduct).filter(CartProduct.product_id == product_id, CartProduct.cart_id == str(cart.id)).first()

    # If cart product exists, update the quantity
    if cart_product:
        cart_product.quantity = quantity
    else:
        # If cart product doesn't exist, create a new one
        new_cart_product = CartProduct(cart_id=str(cart.id), product_id=product_id, quantity=quantity)
        db.add(new_cart_product)

    # Commit changes
    db.commit()
    db.refresh(cart)

    return {"message": "Item added to cart successfully"}

@router.put("/update")
def update_cart(product_id: str, quantity: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if the user has a cart
    cart = db.query(Cart).filter(Cart.user_id == str(current_user.id)).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Check if the product is already in the cart
    cart_product = db.query(CartProduct).filter(CartProduct.product_id == product_id, CartProduct.cart_id == str(cart.id)).first()

    #remove product if product qantity less then 1
    if cart_product.quantity < 1:
        cart_product.delete()
        return {"message": "Removed your product from cart"}

    if cart_product:
        # Update the quantity of the existing product in the cart
        cart_product.quantity = quantity

        # Commit changes
        db.commit()
        db.refresh(cart_product)

        return {"message": "Cart updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Product not found in the cart")


@router.delete("/clear")
def clear_cart(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == str(current_user.id)).first()

    if cart:
        # Delete all CartProduct entries related to the cart
        db.query(CartProduct).filter(CartProduct.cart_id == str(cart.id)).delete()

        # Commit changes
        db.commit()
        db.refresh(cart)

        return {"message": "Cart cleared successfully"}
    else:
        raise HTTPException(status_code=404, detail="Cart not found")

