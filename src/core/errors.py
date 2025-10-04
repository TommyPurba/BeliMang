# src/core/errors.py
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

async def validation_exception_handler(request: Request, exc: ValidationError):
    # gabungkan pesan singkat
    msg = "; ".join([f"{e['loc'][-1]}: {e['msg']}" for e in exc.errors()])
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"error": "ValidationError", "message": msg},
    )

async def auth_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTP_401_UNAUTHORIZED,
        content={"error": "Unauthorized", "message": "Missing or invalid Authorization token"},
    )
