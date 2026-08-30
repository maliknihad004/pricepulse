from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.products import router as product_router
from app.db.database import Base, engine
from app.models.product import Product

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PricePulse API",
    description="Smart product price tracking API",
    version="1.0.0",
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# ROUTES
# --------------------------------------------------

app.include_router(product_router)


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "PricePulse API is running",
        "status": "healthy",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }