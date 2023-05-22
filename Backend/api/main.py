from fastapi import FastAPI
from routes import User


app = FastAPI()

app.include_router(User.router)