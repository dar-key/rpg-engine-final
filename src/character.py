from item import Item


class Character:
    """
    Represents a playable character in the RPG Engine.

    Attributes:
        name         (str)   : Character name
        level        (int)   : Current level (starts at 1)
        strength     (int)   : Affects base damage
        dexterity    (int)   : Affects speed
        intelligence (int)   : Affects magic / future abilities
        max_hp       (int)   : Maximum health points
        hp           (int)   : Current health points
        gold         (int)   : Currency
        experience   (int)   : XP towards next level
        inventory    (list)  : List of Item objects
        equipped     (dict)  : Slots -> Item or None
        speed_formula(str)   : Formula preset for speed calculation
    """

    SPEED_FORMULAS = {
        "default":   lambda dex, items_bonus: dex * 0.5 + items_bonus,
        "agile":     lambda dex, items_bonus: dex * 1.0 + items_bonus,
        "slow":      lambda dex, items_bonus: dex * 0.25 + items_bonus,
    }

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

    # ── Derived stats ────────────────────────────────────────────────

    @property
    def speed(self) -> float:
        """Speed determines turn order in combat."""
        bonus = self.equipped["armor"].speed_effect if self.equipped["armor"] else 0
        formula = self.SPEED_FORMULAS.get(self.speed_formula,
                                          self.SPEED_FORMULAS["default"])
        return formula(self.dexterity, bonus)

    @property
    def damage(self) -> float:
        """Base damage output."""
        weapon_bonus = self.equipped["weapon"].attack_effect if self.equipped["weapon"] else 0
        return self.strength * 1.5 + self.dexterity * 0.5 + weapon_bonus

    @property
    def max_hp_total(self) -> int:
        """Max HP including armor bonuses."""
        armor_bonus = self.equipped["armor"].hp_effect if self.equipped["armor"] else 0
        return self.max_hp + armor_bonus

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

    # ── Combat ───────────────────────────────────────────────────────

    def take_damage(self, amount: float):
        """Reduce HP by amount. HP cannot go below 0."""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        if not self.is_alive():
            print(f"  {self.name} has been defeated!")

    def is_alive(self) -> bool:
        return self.hp > 0

    def heal(self, amount: float):
        """Restore HP without exceeding max."""
        self.hp = min(self.hp + amount, self.max_hp_total)

    def restore_full(self):
        """Full heal (used after dungeon / between encounters)."""
        self.hp = self.max_hp_total

    # ── Levelling ────────────────────────────────────────────────────

    def gain_experience(self, amount: int):
        self.experience += amount
        print(f"  {self.name} gained {amount} XP. ({self.experience}/{self.level * 100})")
        while self.experience >= self.level * 100:
            self.level_up()

    def level_up(self):
        self.experience -= self.level * 100   # carry over excess XP
        self.level += 1
        self.strength += 2
        self.dexterity += 2
        self.intelligence += 2
        self.max_hp += 10
        self.restore_full()
        print(f"  *** LEVEL UP! {self.name} is now level {self.level}! ***")

    # ── Equipment ────────────────────────────────────────────────────

    def equip(self, item: "Item") -> bool:
        """
        Equip an item from inventory.
        Returns True on success, False if item not in inventory or wrong type.
        """
        if item not in self.inventory:
            print(f"  {item.name} is not in your inventory.")
            return False
        slot = item.item_type  # "weapon" or "armor"
        if slot not in self.equipped:
            print(f"  Cannot equip item of type '{slot}'.")
            return False
        self.equipped[slot] = item
        print(f"  Equipped: {item.name}")
        return True

    def unequip(self, slot: str) -> bool:
        """Unequip item from given slot ('weapon' or 'armor')."""
        if slot not in self.equipped or self.equipped[slot] is None:
            print(f"  Nothing equipped in '{slot}' slot.")
            return False
        print(f"  Unequipped: {self.equipped[slot].name}")
        self.equipped[slot] = None
        return True

    # ── Economy ──────────────────────────────────────────────────────

    def add_item(self, item: "Item"):
        self.inventory.append(item)

    def remove_item(self, item: "Item") -> bool:
        if item in self.inventory:
            # Auto-unequip if removing equipped item
            for slot, equipped_item in self.equipped.items():
                if equipped_item is item:
                    self.equipped[slot] = None
            self.inventory.remove(item)
            return True
        return False

    def can_afford(self, price: int) -> bool:
        return self.gold >= price

    def spend_gold(self, amount: int) -> bool:
        if self.can_afford(amount):
            self.gold -= amount
            return True
        print("  Not enough gold!")
        return False

    def earn_gold(self, amount: int):
        self.gold += amount

    # ── Speed formula ────────────────────────────────────────────────

    def set_speed_formula(self, formula_name: str) -> bool:
        """
        Change the speed formula. Available: 'default', 'agile', 'slow'.
        This is the ENGINE feature — lets users customise how speed is calculated.
        """
        if formula_name in self.SPEED_FORMULAS:
            self.speed_formula = formula_name
            print(f"  Speed formula set to: {formula_name}")
            return True
        print(f"  Unknown formula '{formula_name}'. Options: {list(self.SPEED_FORMULAS.keys())}")
        return False

    # ── Serialisation (used by save.py) ──────────────────────────────

    def to_dict(self) -> dict:
        return {
            "name":          self.name,
            "level":         self.level,
            "strength":      self.strength,
            "dexterity":     self.dexterity,
            "intelligence":  self.intelligence,
            "max_hp":        self.max_hp,
            "hp":            self.hp,
            "gold":          self.gold,
            "experience":    self.experience,
            "speed_formula": self.speed_formula,
            "inventory":     [item.to_dict() for item in self.inventory],
            "equipped": {
                slot: (item.name if item else None)
                for slot, item in self.equipped.items()
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Character":
        from item import Item
        char = cls(
            name         = data["name"],
            strength     = data["strength"],
            dexterity    = data["dexterity"],
            intelligence = data["intelligence"],
            hp           = data["max_hp"],
            gold         = data["gold"],
        )
        char.level        = data["level"]
        char.hp           = data["hp"]
        char.experience   = data["experience"]
        char.speed_formula = data.get("speed_formula", "default")
        char.inventory    = [Item.from_dict(i) for i in data.get("inventory", [])]

        # Re-link equipped items by name
        equipped_names = data.get("equipped", {})
        for slot, item_name in equipped_names.items():
            if item_name:
                for item in char.inventory:
                    if item.name == item_name:
                        char.equipped[slot] = item
                        break
        return char