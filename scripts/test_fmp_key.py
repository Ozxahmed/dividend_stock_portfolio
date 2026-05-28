import os
import requests
from dotenv import load_dotenv


def get_required_env_var(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise ValueError(f"Missing required environment variable: {name}")

    return value


def main():
    load_dotenv()

    api_key = get_required_env_var("FMP_API_KEY")

    url = "https://financialmodelingprep.com/stable/profile"
    params = {
        "symbol": "AAPL",
        "apikey": api_key,
    }

    response = requests.get(url, params=params, timeout=30)

    print("Final URL without key:")
    print(response.url.replace(api_key, "REDACTED"))

    print("\nStatus code:")
    print(response.status_code)

    print("\nResponse preview:")
    print(response.text[:1000])


if __name__ == "__main__":
    main()