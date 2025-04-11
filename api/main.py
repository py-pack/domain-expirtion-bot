import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.tools import check_domain

app = FastAPI()


@app.middleware("http")
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


app.include_router(router=check_domain.router, prefix='/api')


@app.get("/")
async def root():
    # return StreamingResponse('')
    return {"message": "Hello from FastAPI in Docker!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10432, reload=True)
