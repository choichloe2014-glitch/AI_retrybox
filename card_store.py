
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

def update_card(box_name, changed_card):
    cards = load_cards(box_name)
    for i in range(len(cards)):
        if cards[i]["id"] == changed_card["id"]:
            cards[i] = changed_card
    save_cards(box_name, cards)