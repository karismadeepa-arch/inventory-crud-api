# Inventory Product CRUD API

FastAPI project implementing:

- User registration
- Argon2 password hashing
- JWT login
- JWT authentication dependency
- Product CRUD
- User ownership
- Pagination
- Pydantic validation
- SQLite database

## Run

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open:

http://127.0.0.1:8000/docs

## API endpoints

POST /register
POST /login
GET /me

POST /products
GET /products?page=1&limit=10
GET /products/{product_id}
PUT /products/{product_id}
DELETE /products/{product_id}

## Test order

1. Register a user.
2. Login.
3. Copy the JWT access token.
4. Click Authorize in Swagger.
5. Enter: Bearer YOUR_TOKEN
6. Create and manage products.

Products are automatically linked to the logged-in user. A user cannot access another user's products.
