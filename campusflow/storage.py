import json
import os


def load_tickets(filepath: str) -> list:
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("JSON root element must be a list of tickets.")
            return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Corrupted storage file at {filepath}: {str(e)}")


def save_tickets(filepath: str, tickets: list) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2)