# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models  # ensure this imports your models module so Base is defined
from database import engine, Base
from routers import users, books, activity


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Readify API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],  # update to more specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(books.router)
app.include_router(activity.router)
