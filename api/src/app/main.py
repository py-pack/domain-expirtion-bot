import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infra.http.middleware import response_format_middleware

from app.domains.tools.router import tools_router
from app.domains.auth.router import auth_router
from app.domains.users.router import users_router
from app.domains.units.router import units_router
from app.domains.account_domains.router import account_domains_router

from app.core.config import settings

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
app.include_router(router=users_router, prefix='/api/v1/users', tags=['users'])
app.include_router(router=units_router, prefix='/api/v1/units', tags=['units'])
app.include_router(router=account_domains_router, prefix='/api/v1/account-domains', tags=['account-domains'])


@app.get("/")
async def root():
    # return StreamingResponse('')
    return {"message": "Hello from FastAPI in Docker!"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=10431, reload=True)
