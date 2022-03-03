# Python
import os
# FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# SqlAlchemy
from config.db import engine


# Routes Loan
from modules.clients import routes as routes_clients
from modules.loans import routes as routes_loans
from modules.amortization import routes as routes_amortization


# Models
from modules.clients import models as model_clients
from modules.loans import models as model_loans


# Create tables for APP
model_clients.Base.metadata.create_all(bind=engine)
model_loans.Base.metadata.create_all(bind=engine)


origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://micoloans.netlify.app",
    "https://micoloans.herokuapp.com"
]


# Conf API
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_clients.router)
app.include_router(routes_loans.router)
app.include_router(routes_amortization.router)


# Home
@app.get(path="/")
def home():
    return {"msg": "app running"}
