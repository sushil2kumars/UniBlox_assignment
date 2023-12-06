
from app import app
from routes import user, product, cart
from models import Base
from app import engine


Base.metadata.create_all(bind=engine)


app.include_router(user.router, prefix="/user", tags=["auth"])
app.include_router(product.router, prefix="/product", tags=["auth"])
app.include_router(cart.router, prefix="/cart", tags=["auth"])




if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)