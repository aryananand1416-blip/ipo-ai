
from fastapi import FastAPI

from app.routes.predict import (
    router as prediction_router
)

from app.routes.ranking import (
    router as ranking_router
)

from app.routes.ipos import (
    router as ipo_router
)


app = FastAPI(
    title="IPO AI API",
    version="IPO_AI_v1",
    description=(
        "AI-powered Indian IPO ranking "
        "and prediction API"
    )
)


# ------------------------------------------------------------
# Routers
# ------------------------------------------------------------

app.include_router(
    prediction_router
)

app.include_router(
    ranking_router
)

app.include_router(
    ipo_router
)


# ------------------------------------------------------------
# Root
# ------------------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "IPO AI API is running",
        "version": "IPO_AI_v1"
    }


# ------------------------------------------------------------
# Health
# ------------------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "ok",
        "model_version": "IPO_AI_v1"
    }
