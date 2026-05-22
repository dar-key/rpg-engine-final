import json
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from character import Character
    from shop import Shop

SAVE_DIR = "saves"
SAVE_FILE = os.path.join(SAVE_DIR, "savegame.json")


def _ensure_save_dir():
    os.makedirs(SAVE_DIR, exist_ok=True)


def save_game(character: "Character", shop: "Shop") -> bool:
    _ensure_save_dir()
    data = {
        "character": character.to_dict(),
        "shop": shop.to_dict(),
    }
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  Game saved to {SAVE_FILE}")
        return True
    except OSError as e:
        print(f"  Save failed: {e}")
        return False


def load_game() -> tuple["Character", "Shop"] | None:
    from character import Character
    from shop import Shop

    if not os.path.exists(SAVE_FILE):
        print("  No save file found.")
        return None

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        character = Character.from_dict(data["character"])
        shop = Shop.from_dict(data["shop"])
        print(f"  Game loaded from {SAVE_FILE}.")
        return character, shop
    except (KeyError, ValueError, json.JSONDecodeError) as e:
        print(f"  Save file is corrupt or incompatible: {e}")
        return None


def save_exists() -> bool:
    return os.path.exists(SAVE_FILE)


def delete_save() -> bool:
    if save_exists():
        os.remove(SAVE_FILE)
        print("  Save file deleted.")
        return True
    print("  No save file to delete.")
    return False
