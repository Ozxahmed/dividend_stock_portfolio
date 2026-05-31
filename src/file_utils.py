"""
Utility functions for file operations- saving/loading files.
"""


import json
from datetime import datetime
from pathlib import Path


def save_json(
    data: dict | list,
    symbol: str,
    dataset_name: str,
    folder_path: str = "data/raw/fmp",
) -> Path:
    project_root = Path(__file__).resolve().parents[1]
    today = datetime.now().strftime("%Y-%m-%d")

    filename = f"{dataset_name}_{symbol}_{today}.json"
    target_dir = project_root / folder_path
    full_path = target_dir / filename

    full_path.parent.mkdir(parents=True, exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Saved: {full_path}")
    return full_path