import whois
from datetime import datetime, timezone
from dateutil import parser

from http import HTTPStatus
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.api_setting import AUTHORISATION

tools_router: APIRouter = APIRouter(dependencies=[AUTHORISATION])


@tools_router.get(path="/expiration", status_code=HTTPStatus.OK)
async def get_domain_info(domain_name: str):
    domain_info = whois.whois(domain_name)

    if not domain_info.expiration_date:
        raise Exception("Expiration date not found.")

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "data": {
                "domain": domain_name,
                "expiration_date": _parse_expiration_date(domain_info.expiration_date)
            }
        })


def _parse_expiration_date(expiration_date) -> str:
    if isinstance(expiration_date, list):
        dates = []
        for date in expiration_date:
            if isinstance(expiration_date, str):
                dates.append(parser.parse(date))
            else:
                dates.append(date)
        dates = [dt.astimezone(timezone.utc) if dt.tzinfo else dt.replace(tzinfo=timezone.utc) for dt in expiration_date]

        result = min(dates)
    elif isinstance(expiration_date, str):
        result = parser.parse(expiration_date)
    elif isinstance(expiration_date, datetime):
        result = expiration_date
    else:
        raise ValueError("Failed to parse expiration date.")

    return result.strftime("%Y-%m-%d %H:%M:%S")
