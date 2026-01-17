from fastapi import Request, Depends, HTTPException
from http import HTTPStatus

from app.core.config import settings

async def authorisation(request: Request):
    if request.headers.get("Token-X") != settings.x_token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Not authorised",
        )

AUTHORISATION = Depends(authorisation)
