from item import Item


class Character:

    def __init__(self, name: str, strength: int = 5, dexterity: int = 5,
                 intelligence: int = 5, hp: int = 100, gold: int = 50):
        self.name = name
        self.level = 1
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.max_hp = hp
        self.hp = hp
        self.gold = gold
        self.experience = 0
        self.inventory: list[Item] = []
        self.equipped: dict[str, Item | None] = {
            "weapon": None,
            "armor": None,
        }
        self.speed_formula = "default"

    # ── Display ──────────────────────────────────────────────────────

    def show_stats(self):
        sep = "=" * 32
        print(sep)
        print(f"  {self.name}  |  Level {self.level}")
        print(sep)
        print(f"  HP          : {self.hp} / {self.max_hp_total}")
        print(f"  Strength    : {self.strength}")
        print(f"  Dexterity   : {self.dexterity}")
        print(f"  Intelligence: {self.intelligence}")
        print(f"  Damage      : {self.damage:.1f}")
        print(f"  Speed       : {self.speed:.1f}  (formula: {self.speed_formula})")
        print(f"  Gold        : {self.gold}g")
        print(f"  XP          : {self.experience} / {self.level * 100}")
        print(f"  Weapon      : {self.equipped['weapon'].name if self.equipped['weapon'] else 'None'}")
        print(f"  Armor       : {self.equipped['armor'].name  if self.equipped['armor']  else 'None'}")
        print(sep)

    def show_inventory(self):
        if not self.inventory:
            print("  Inventory is empty.")
            return
        print("=== Inventory ===")
        for i, item in enumerate(self.inventory, 1):
            equipped_tag = ""
            if item is self.equipped.get("weapon"):
                equipped_tag = " [E-Weapon]"
            elif item is self.equipped.get("armor"):
                equipped_tag = " [E-Armor]"
            print(f"  {i}. {item.name}{equipped_tag}  ({item.item_type}, {item.price}g)")

