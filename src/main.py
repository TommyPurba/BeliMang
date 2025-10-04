from fastapi import FastAPI
from src.merchants.database import Base, engine   # pakai merchants Base
from src.merchants import models                  # pastikan model terimport
from src.merchants.router import router as merchants_router

app = FastAPI(title="BeliMang!", version="1.0.0")

# ✅ gunakan nama alias yang benar
app.include_router(merchants_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to BeliMang!"}
