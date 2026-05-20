# items.py
# RPG Engine — Items module
# Author: [YourName]

from typing import Optional


# Allowed item types and their valid effect fields
ITEM_TYPES = {
    "weapon": ["attack_effect", "speed_effect"],
    "armor":  ["hp_effect", "speed_effect"],
    "potion": ["hp_effect"],
}

RARITIES = ["common", "uncommon", "rare", "epic", "legendary"]


class Item:
    """
    Represents an in-game item.

    Attributes:
        name          (str)  : Display name
        item_type     (str)  : 'weapon', 'armor', or 'potion'
        rarity        (str)  : One of RARITIES
        price         (int)  : Gold cost in the shop
        description   (str)  : Flavour text
        attack_effect (int)  : Bonus damage (weapons)
        hp_effect     (int)  : Bonus/heal HP (armor, potions)
        speed_effect  (int)  : Speed modifier (weapons, armor)
    """

    def __init__(
        self,
        name: str,
        item_type: str,
        price: int,
        description: str = "",
        rarity: str = "common",
        attack_effect: int = 0,
        hp_effect: int = 0,
        speed_effect: int = 0,
    ):
        if item_type not in ITEM_TYPES:
            raise ValueError(f"Invalid item_type '{item_type}'. Must be: {list(ITEM_TYPES.keys())}")
        if rarity not in RARITIES:
            raise ValueError(f"Invalid rarity '{rarity}'. Must be: {RARITIES}")

        self.name = name
        self.item_type = item_type
        self.price = max(0, price)
        self.description = description
        self.rarity = rarity
        self.attack_effect = attack_effect
        self.hp_effect = hp_effect
        self.speed_effect = speed_effect

    # ── Display ──────────────────────────────────────────────────────

    def show(self):
        sep = "-" * 30
        print(sep)
        print(f"  {self.name}  [{self.rarity.upper()}]")
        print(f"  Type   : {self.item_type}")
        print(f"  Price  : {self.price}g")
        if self.attack_effect:
            print(f"  Attack : +{self.attack_effect}")
        if self.hp_effect:
            print(f"  HP     : +{self.hp_effect}")
        if self.speed_effect != 0:
            sign = "+" if self.speed_effect > 0 else ""
            print(f"  Speed  : {sign}{self.speed_effect}")
        if self.description:
            print(f"  \"{self.description}\"")
        print(sep)

    def __repr__(self) -> str:
        return (f"Item({self.name!r}, type={self.item_type}, "
                f"rarity={self.rarity}, price={self.price}g)")

    # ── Serialisation (used by save.py) ──────────────────────────────

    def to_dict(self) -> dict:
        return {
            "name":          self.name,
            "item_type":     self.item_type,
            "price":         self.price,
            "description":   self.description,
            "rarity":        self.rarity,
            "attack_effect": self.attack_effect,
            "hp_effect":     self.hp_effect,
            "speed_effect":  self.speed_effect,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        return cls(
            name          = data["name"],
            item_type     = data["item_type"],
            price         = data["price"],
            description   = data.get("description", ""),
            rarity        = data.get("rarity", "common"),
            attack_effect = data.get("attack_effect", 0),
            hp_effect     = data.get("hp_effect", 0),
            speed_effect  = data.get("speed_effect", 0),
        )


# ── Default item catalogue (also written to items_data.json by save.py) ──────

DEFAULT_ITEMS: list[Item] = [
    Item("Rusty Sword",    "weapon", price=20,  description="Better than nothing.",
         rarity="common",    attack_effect=5),
    Item("Iron Sword",     "weapon", price=60,  description="Standard soldier issue.",
         rarity="uncommon",  attack_effect=12, speed_effect=1),
    Item("Shadow Blade",   "weapon", price=150, description="Light and deadly.",
         rarity="rare",      attack_effect=18, speed_effect=5),
    Item("Leather Armor",  "armor",  price=25,  description="Flexible, light protection.",
         rarity="common",    hp_effect=15),
    Item("Chain Mail",     "armor",  price=80,  description="Solid mid-tier armor.",
         rarity="uncommon",  hp_effect=30, speed_effect=-2),
    Item("Dragon Scale",   "armor",  price=200, description="Forged from dragon hide.",
         rarity="rare",      hp_effect=60, speed_effect=-1),
    Item("Small Potion",   "potion", price=15,  description="Restores 30 HP.",
         rarity="common",    hp_effect=30),
    Item("Large Potion",   "potion", price=40,  description="Restores 75 HP.",
         rarity="uncommon",  hp_effect=75),
]