from fastapi import FastAPI, Request,Form,Depends,Query
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel
from pwdlib import PasswordHash
from database import engine, Base,SessionLocal
from models import RegisterForm
DATABASE_URL = "sqlite:///./task.db"
password_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, saved_hash: str) -> bool:
    return password_hasher.verify(password, saved_hash)

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
#this function helps to create temp connection between backend and server
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Inputtype(BaseModel):
        first_name:str
        last_name:str
        phone_number:str
        email:str
        gender:str
        city:str
        role:str
        password:str

class LoginInput(BaseModel):
        email:str
        password:str

@app.get("/", response_class=HTMLResponse)
def home(req: Request):
    return templates.TemplateResponse(
        request=req,
        name="login.html",

    )
@app.get("/register", response_class=HTMLResponse)
def home(req: Request):
    return templates.TemplateResponse(
        request=req,
        name="register.html",

    )

@app.post('/register')
def register(user:Annotated[Inputtype,Form()],db=Depends(get_db)):
    new_user = RegisterForm(
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        email=user.email,
        gender=user.gender,
        city=user.city,
        role=user.role,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return RedirectResponse(
         url='/',
        status_code=303
    )

@app.post('/login')
def login(user: Annotated[LoginInput, Form()], db: Session = Depends(get_db)):

    existing_user = db.query(RegisterForm).filter(
        RegisterForm.email == user.email
    ).first()

    if not existing_user:
        return {"message": "Email not registered"}

    if verify_password(user.password, existing_user.password):

        return RedirectResponse(
            url='/dashboard',
            status_code=303
        )

    return {"message": "Incorrect password"}