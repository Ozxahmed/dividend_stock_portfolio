import os
from pathlib import Path

from dotenv import load_dotenv
from schwab import auth  # type: ignore


def main():
    load_dotenv()

    app_key = os.getenv("SCHWAB_APP_KEY")
    app_secret = os.getenv("SCHWAB_APP_SECRET")
    callback_url = os.getenv("SCHWAB_CALLBACK_URL")
    token_path = os.getenv("SCHWAB_TOKEN_PATH", ".secrets/schwab_token.json")

    if not app_key:
        raise ValueError("Missing SCHWAB_APP_KEY in .env")

    if not app_secret:
        raise ValueError("Missing SCHWAB_APP_SECRET in .env")

    if not callback_url:
        raise ValueError("Missing SCHWAB_CALLBACK_URL in .env")

    Path(token_path).parent.mkdir(parents=True, exist_ok=True)

    print("Starting Schwab authentication...")
    print(f"Callback URL: {callback_url}")
    print(f"Token path: {token_path}")

    auth.easy_client(
        api_key=app_key,
        app_secret=app_secret,
        callback_url=callback_url,
        token_path=token_path,
    )

    print("Authentication worked.")
    print("Client created successfully.")


if __name__ == "__main__":
    main()
