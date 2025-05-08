from fastapi import FastAPI, Request, Depends, HTTPException, status, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List
import json

from models.user import User
from models.flower import Flower
from repositories.users import UsersRepository
from repositories.flowers import FlowersRepository
from repositories.purchases import PurchasesRepository

app = FastAPI()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

users_repository = UsersRepository()
flowers_repository = FlowersRepository()
purchases_repository = PurchasesRepository()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

templates = Jinja2Templates(directory="templates")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = users_repository.get_by_email(username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/signup")
async def signup(
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        photo: UploadFile = File(None)
):
    hashed_password = get_password_hash(password)
    photo_url = None

    if photo:
        # Сохраняем фото и получаем URL
        photo_url = f"uploads/{photo.filename}"
        with open(photo_url, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

    user = users_repository.create(username, email, hashed_password, photo_url)
    return {"status": "OK"}


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_repository.get_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": current_user
    })


@app.get("/flowers", response_class=HTMLResponse)
async def get_flowers(request: Request):
    flowers = flowers_repository.get_all()
    return templates.TemplateResponse("flowers.html", {
        "request": request,
        "flowers": flowers
    })


@app.post("/flowers")
async def add_flower(
        name: str = Form(...),
        cost: float = Form(...),
        count: int = Form(...)
):
    flower = flowers_repository.create(name, cost, count)
    return {"id": flower.id}


@app.post("/cart/items")
async def add_to_cart(
        flower_id: int = Form(...),
        cart: Optional[str] = Cookie(None)
):
    cart_items = json.loads(cart) if cart else []
    cart_items.append(flower_id)
    response = RedirectResponse(url="/cart/items", status_code=303)
    response.set_cookie(key="cart", value=json.dumps(cart_items))
    return response


@app.get("/cart/items", response_class=HTMLResponse)
async def get_cart(request: Request, cart: Optional[str] = Cookie(None)):
    cart_items = json.loads(cart) if cart else []
    flowers = flowers_repository.get_by_ids(cart_items)
    total = sum(flower.cost for flower in flowers)
    return templates.TemplateResponse("cart.html", {
        "request": request,
        "flowers": flowers,
        "total": total
    })


@app.post("/purchased")
async def purchase_items(
        current_user: User = Depends(get_current_user),
        cart: Optional[str] = Cookie(None)
):
    cart_items = json.loads(cart) if cart else []
    for flower_id in cart_items:
        purchases_repository.create(current_user.id, flower_id)

    response = RedirectResponse(url="/purchased", status_code=303)
    response.delete_cookie("cart")
    return response


@app.get("/purchased", response_class=HTMLResponse)
async def get_purchased(
        request: Request,
        current_user: User = Depends(get_current_user)
):
    purchases = purchases_repository.get_by_user_id(current_user.id)
    flower_ids = [purchase.flower_id for purchase in purchases]
    flowers = flowers_repository.get_by_ids(flower_ids)
    return templates.TemplateResponse("purchased.html", {
        "request": request,
        "flowers": flowers
    })