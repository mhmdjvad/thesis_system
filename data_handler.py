import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).parent / "data"

def load_json(fn: str, default: Any):
    """Load JSON file or return default if missing or corrupted."""
    try:
        with open(DATA_DIR / fn, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {fn} not found. Using default data.")
        return default
    except Exception as e:
        print(f"Warning: Failed to load {fn}. Reason: {e}. Using default data.")
        return default

def save_json(fn: str, data: Any):
    """Save data as pretty JSON to file."""
    with open(DATA_DIR / fn, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)