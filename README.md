# UniBlox  Assinment

This is a simple FastAPI project for e-commerce functionalities, including user authentication, product management, and cart functionality.

## Prerequisites

- Python 3.7 or higher installed
- Git installed
- (Optional) A virtual environment for Python

## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/fastapi-ecommerce.git
    cd fastapi-ecommerce
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up the database:

    ```bash
    # Create the initial database
    python -m alembic upgrade head
    ```

4. Run the FastAPI application:

    ```bash
    uvicorn main:app --reload
    ```

    The application should be running at `http://127.0.0.1:8000`. Visit this URL in your browser to interact with the API.





# Postman requests collections 
To use these request, you need to import them into your postman client from this link [here](https://api.postman.com/collections/8771699-074db1e8-e01f-4966-afb6-b902cd65ffca?access_key=PMAT-01HH2NCZ9HZEQ92V56DJNSSXQX).



# UniBlox API Documentation

## User Endpoints

### Signup
- **POST** `http://127.0.0.1:8000/user/signup`
- **Query Params:**
  - username
  - password

### Signin
- **POST** `http://127.0.0.1:8000/user/signin`
- **Query Params:**
  - username
  - password

## Product Endpoints

### Add New Product
- **POST** `http://127.0.0.1:8000/product/`
- **Request Headers:**
  - Authorization (Bearer Token)
- **Body:**
  - JSON: {"name": "Test 4", "price": 500}

### Update Product
- **PUT** `http://127.0.0.1:8000/product/{product_id}`
- **Request Headers:**
  - Authorization (Bearer Token)
- **Body:**
  - JSON: {"name": "Test 4", "price": 550.0}

### Delete Product
- **DELETE** `http://127.0.0.1:8000/product/{product_id}`
- **Request Headers:**
  - Authorization (Bearer Token)

## Cart Endpoints

### Add Product to Cart
- **POST** `http://127.0.0.1:8000/cart/`
- **Request Headers:**
  - Authorization (Bearer Token)
- **Query Params:**
  - product_id
  - quantity

### Get Product List in Cart
- **GET** `http://127.0.0.1:8000/cart`
- **Request Headers:**
  - Authorization (Bearer Token)

### Update Cart Product
- **PUT** `http://127.0.0.1:8000/cart/update/`
- **Request Headers:**
  - Authorization (Bearer Token)
- **Query Params:**
  - product_id
  - quantity

### Checkout
- **POST** `http://127.0.0.1:8000/cart/checkout`
- **Request Headers:**
  - Authorization (Bearer Token)

## Admin Endpoints

### Add New Coupons
- **POST** `http://127.0.0.1:8000/admin/coupons/`
- **Request Headers:**
  - Authorization (Bearer Token)
- **Body:**
  - JSON: {"code": "HOT10", "nth_order": 10, "discount_percent": 10}

### Get All Coupons
- **GET** `http://127.0.0.1:8000/admin/coupons/`
- **Request Headers:**
  - Authorization (Bearer Token)

### Delete Coupon
- **DELETE** `http://127.0.0.1:8000/admin/coupons/{coupon_id}`
- **Request Headers:**
  - Authorization (Bearer Token)

### Purchase Statistics
- **GET** `http://127.0.0.1:8000/admin/purchase_statistics`
- **Request Headers:**
  - Authorization (Bearer Token)