from http import HTTPStatus
from typing import NoReturn
from fastapi import Request, Depends, HTTPException

from app.config import settings


async def authorisation(request: Request) -> NoReturn | None:
    if request.headers.get("Token-X") != settings.x_token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Not authorised'
        )


AUTHORISATION: Depends = Depends(dependency=authorisation)
