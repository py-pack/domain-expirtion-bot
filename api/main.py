import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api_setting import response_format_middleware

from src.tools.router import tools_router
from src.auth.router import auth_router

from settings import settings

app = FastAPI(title="Domain Expiration Bot")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=settings.api.allow_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(response_format_middleware)

app.include_router(router=tools_router, prefix='/api/domain', tags=['tools'])
app.include_router(router=auth_router, prefix='/api/v1/auth', tags=['auth'])


@app.get("/")
async def root():
    # return StreamingResponse('')
    return {"message": "Hello from FastAPI in Docker!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10431, reload=True)
