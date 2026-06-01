"""
Environment variables / project settings
"""

import os
from pathlib import Path

from dotenv import load_dotenv


def load_env_variable(name: str) -> str:
    project_root = Path(__file__).resolve().parents[1]

    env_path = project_root / ".env"

    load_dotenv(dotenv_path=env_path)

    value = os.getenv(name)

    if not value:
        raise ValueError(f"Missing required env variable: {name}")

    return value
