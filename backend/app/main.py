from fastapi import FastAPI

from .routers import auth, measure, payments, stores

app = FastAPI(title="ShoeFlow AI Measurement Marketplace")

app.include_router(measure.router, prefix="/api/measure", tags=["measure"])
app.include_router(stores.router, prefix="/api/stores", tags=["stores"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(payments.router, prefix="/api/payments", tags=["payments"])


@app.get("/")
def read_root():
    return {"message": "ShoeFlow AI Measurement Marketplace API"}
