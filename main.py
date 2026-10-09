from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import User, Product
from auth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from schemas import (
    UserRegister,
    UserResponse,
    LoginRequest,
    TokenResponse,
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)
from auth import hash_password, verify_password, create_access_token, get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory Product CRUD API",
    description="FastAPI CRUD application with JWT authentication",
    version="1.0.0",
)


@app.get("/")
def home():
    return {"message": "Inventory Product CRUD API is running"}


@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=409, detail="Username already exists")

    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=409, detail="Email already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(username=user.username, user_id=user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
        owner_id=current_user.id,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.get("/products", response_model=list[ProductResponse])
def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skip = (page - 1) * limit

    return (
        db.query(Product)
        .filter(Product.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.owner_id == current_user.id)
        .first()
    )

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.owner_id == current_user.id)
        .first()
    )

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.quantity = product_data.quantity

    db.commit()
    db.refresh(product)
    return product


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.owner_id == current_user.id)
        .first()
    )

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return None
