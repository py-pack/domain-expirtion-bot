from fastapi import Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from http import HTTPStatus
from typing import NoReturn

from settings import settings


async def response_format_middleware(request: Request, call_next):
    try:
        response = await call_next(request)

        # if 300 <= response.status_code < 600:
        #     original_response = await response.body()
        #     data = original_response.decode('utf-8')
        #     return JSONResponse(
        #         status_code=response.status_code,
        #         content={
        #             "success": False,
        #             "message": str(data)
        #         },
        #     )

        return response

    except Exception as e:
        if isinstance(e, StarletteHTTPException):
            status_code = e.status_code if 400 <= e.status_code <= 600 else 400
            return JSONResponse(
                status_code=status_code,
                content={
                    "success": False,
                    "message": e.detail
                },
            )

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": str(e)
            },
        )


async def authorisation(request: Request) -> NoReturn | None:
    if request.headers.get("Token-X") != settings.x_token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Not authorised'
        )


AUTHORISATION: Depends = Depends(dependency=authorisation)
