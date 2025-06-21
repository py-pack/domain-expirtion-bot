import jwt
from jwt import PyJWKClient
from jwt.exceptions import InvalidTokenError
import requests

GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_ENDPOINT = "https://www.googleapis.com/oauth2/v2/userinfo"

GOOGLE_CERTS_URL = "https://www.googleapis.com/oauth2/v3/certs"
GOOGLE_ISSUERS = ["https://accounts.google.com", "accounts.google.com"]


def get_google_auth_url(client_id: str, redirect_uri: str, scopes: list[str]) -> str:
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scopes.join(" "),
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
    }
    from urllib.parse import urlencode
    return f"{GOOGLE_AUTH_ENDPOINT}?{urlencode(params)}"


def exchange_code_for_token(code: str, client_id: str, client_secret: str, redirect_uri: str) -> dict:
    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    resp = requests.post(GOOGLE_TOKEN_ENDPOINT, data=data)
    try:
        resp.raise_for_status()
    except requests.HTTPError:
        print("Google token error:", resp.text)  # ДОДАЙ це
        raise
    return resp.json()


def get_user_email_from_google(code: str, client_id: str, client_secret: str, redirect_uri: str) -> dict:
    access_token_obj = exchange_code_for_token(code, client_id, client_secret, redirect_uri)
    access_token = access_token_obj.get("access_token")

    if not access_token:
        raise ValueError("Invalid access token")

    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(GOOGLE_USERINFO_ENDPOINT, headers=headers)
    try:
        resp.raise_for_status()
    except requests.HTTPError:
        print("Google token error:", resp.text)  # ДОДАЙ це
        raise

    return resp.json()


def verify_google_token(id_token: str, client_id: str) -> dict:
    try:
        # 1. Отримати ключі від Google
        jwk_client = PyJWKClient(GOOGLE_CERTS_URL)
        signing_key = jwk_client.get_signing_key_from_jwt(id_token)

        # 2. Розшифрувати токен
        payload = jwt.decode(
            id_token,
            signing_key.key,
            algorithms=["RS256"],
            audience=client_id,
            issuer=GOOGLE_ISSUERS,
        )

        # 3. Додаткова перевірка (опційно)
        if not payload.get("email_verified"):
            raise InvalidTokenError("Email not verified")

        return payload

    except Exception as e:
        raise ValueError(f"Invalid ID token: {e}")
