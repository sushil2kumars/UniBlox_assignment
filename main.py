
from app import app
from routes import user, product, cart, checkout_product
from models import Base
from app import engine
from admin import admin_routes


Base.metadata.create_all(bind=engine)


app.include_router(user.router, prefix="/user", tags=["auth"])
app.include_router(product.router, prefix="/product", tags=["auth"])
app.include_router(cart.router, prefix="/cart", tags=["auth"])
app.include_router(checkout_product.router, prefix="/cart", tags=["auth"])
app.include_router(admin_routes.router, prefix="/admin", tags=["auth"])



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)