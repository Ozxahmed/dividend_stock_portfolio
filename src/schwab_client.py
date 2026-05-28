import os
from pathlib import Path

from dotenv import load_dotenv
from schwab import auth # type: ignore


def get_schwab_client():
    load_dotenv()

    app_key = os.getenv("SCHWAB_APP_KEY")
    app_secret = os.getenv("SCHWAB_APP_SECRET")
    callback_url = os.getenv("SCHWAB_CALLBACK_URL")
    token_path = os.getenv("SCHWAB_TOKEN_PATH", ".secrets/schwab_token.json")

    if not app_key:
        raise ValueError("Missing SCHWAB_APP_KEY")

    if not app_secret:
        raise ValueError("Missing SCHWAB_APP_SECRET")

    if not callback_url:
        raise ValueError("Missing SCHWAB_CALLBACK_URL")

    Path(token_path).parent.mkdir(parents=True, exist_ok=True)

    return auth.easy_client(
        api_key=app_key,
        app_secret=app_secret,
        callback_url=callback_url,
        token_path=token_path,
    )