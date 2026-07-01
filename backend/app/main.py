"""Origami FarmOS API entrypoint - handbook Chapter 15 (API Architecture)."""
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import animals, auth, briefing, dairy, feed, flocks, locations, observations, poultry, recommendations
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only; restrict per-environment before Phase 7 pilot (Ch.19)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Standard error envelope - Chapter 15 §15.6."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": str(exc.status_code), "message": exc.detail, "field_errors": None}},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"error": {"code": "422", "message": "Validation error", "field_errors": exc.errors()}},
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


api_prefix = settings.api_v1_prefix
app.include_router(auth.router, prefix=api_prefix)
app.include_router(locations.router, prefix=api_prefix)
app.include_router(animals.router, prefix=api_prefix)
app.include_router(flocks.router, prefix=api_prefix)
app.include_router(observations.router, prefix=api_prefix)
app.include_router(feed.router, prefix=api_prefix)
app.include_router(dairy.router, prefix=api_prefix)
app.include_router(poultry.router, prefix=api_prefix)
app.include_router(recommendations.router, prefix=api_prefix)
app.include_router(briefing.router, prefix=api_prefix)
