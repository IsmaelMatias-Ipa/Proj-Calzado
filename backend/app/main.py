from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, measure, payments, stores

app = FastAPI(title="ShoeFlow AI Measurement Marketplace")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(measure.router, prefix="/api/measure", tags=["measure"])
app.include_router(stores.router, prefix="/api/stores", tags=["stores"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(payments.router, prefix="/api/payments", tags=["payments"])


@app.get("/")
def read_root():
    return {"message": "ShoeFlow AI Measurement Marketplace API"}
