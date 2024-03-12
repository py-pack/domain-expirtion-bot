import whois
from datetime import datetime
from dateutil import parser

from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from tools import AUTHORISATION

router: APIRouter = APIRouter(dependencies=[AUTHORISATION])


@router.get(path="/domain/expiration", status_code=HTTPStatus.OK)
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
                "expiration_date": parse_expiration_date(domain_info.expiration_date)
            }
        })


def parse_expiration_date(expiration_date) -> str:
    if isinstance(expiration_date, list):
        dates = []
        for date in expiration_date:
            if isinstance(expiration_date, str):
                dates.append(parser.parse(date))
            else:
                dates.append(date)

        result = min(dates)
    elif isinstance(expiration_date, str):
        result = parser.parse(expiration_date)
    elif isinstance(expiration_date, datetime):
        result = expiration_date
    else:
        raise ValueError("Failed to parse expiration date.")

    return result.strftime("%Y-%m-%d %H:%M:%S")
