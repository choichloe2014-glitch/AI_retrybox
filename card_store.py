card = {
    "id": "3f9a1c2e",
    "subject": "Math",
    "question": "A shirt costs 20 dollars. It is 15% off. What is the new price?",
    "my_answer": "3 dollars",
    "correct_answer": "17 dollars",
    "note": "I found the discount, not the new price.",
    "created_at": "2026-10-18",
}

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

def card_file(box_name):
    return DATA_DIR / f"{box_name}.json"

def load_cards(box_name):
    path = card_file(box_name)
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    return json.loads(text)

def save_cards(box_name, cards):
    DATA_DIR.mkdir(exist_ok=True)
    text = json.dumps(cards, ensure_ascii=False, indent=2)
    card_file(box_name).write_text(text, encoding="utf-8")