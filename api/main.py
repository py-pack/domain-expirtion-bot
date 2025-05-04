import uvicorn
from fastapi import FastAPI
from src.api_setting import response_format_middleware

from src.tools.router import tools_router
from src.auth.router import auth_router

app = FastAPI()

app.middleware("http")(response_format_middleware)

app.include_router(router=tools_router, prefix='/api', tags=['tools'])
app.include_router(router=auth_router, prefix='/auth', tags=['auth'])


@app.get("/")
async def root():
    # return StreamingResponse('')
    return {"message": "Hello from FastAPI in Docker!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10432, reload=True)
