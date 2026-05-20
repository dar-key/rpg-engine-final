# monster.py
# RPG Engine — Monster module
# Author: Sergey
#
# Course topics covered:
#   Week 1  — variables, data types, f-strings, input/output
#   Week 2  — if/elif/else, while loops
#   Week 3  — lists, dicts (custom_attrs, DEFAULT_MONSTERS)
#   Week 5  — functions with default arguments, type hints
#   Week 6  — class, __init__, instance attributes, methods
#   Week 7  — @property, @classmethod, __repr__, inheritance (BossMonster)
#   Week 8  — module-level constants, importable catalogue

import random


# ── Module-level catalogue (Week 3: dict + list, Week 8: module constant) ────

DEFAULT_MONSTERS: list[dict] = [
    {"name": "Goblin",      "hp": 25,  "strength": 4,  "dexterity": 7,
     "xp_reward": 15, "gold_reward": 8,  "description": "Small but quick."},
    {"name": "Orc",         "hp": 60,  "strength": 10, "dexterity": 4,
     "xp_reward": 35, "gold_reward": 20, "description": "Brute force incarnate."},
    {"name": "Skeleton",    "hp": 35,  "strength": 6,  "dexterity": 5,
     "xp_reward": 20, "gold_reward": 10, "description": "Rattles with every step."},
    {"name": "Dark Mage",   "hp": 45,  "strength": 8,  "dexterity": 6,
     "xp_reward": 40, "gold_reward": 25, "description": "Channels forbidden magic."},
    {"name": "Stone Golem", "hp": 120, "strength": 15, "dexterity": 2,
     "xp_reward": 80, "gold_reward": 50, "description": "Slow, but nearly indestructible."},
]


class Monster:
    """
    Represents an enemy entity.

    Week 6: class definition, __init__, instance attributes
    Week 7: @property for derived stats, @classmethod for alternative constructors
    """

    def __init__(
        self,
        name: str,
        hp: int = 30,
        strength: int = 5,
        dexterity: int = 5,
        speed_bonus: float = 0.0,
        xp_reward: int = 20,
        gold_reward: int = 10,
        description: str = "",
    ):
        # Week 1: variables and data types
        self.name: str = name
        self.max_hp: int = max(1, hp)
        self.hp: int = self.max_hp
        self.strength: int = strength
        self.dexterity: int = dexterity
        self.speed_bonus: float = speed_bonus
        self.xp_reward: int = xp_reward
        self.gold_reward: int = gold_reward
        self.description: str = description

        # Week 3: dict — ENGINE feature: user can attach any extra attribute
        self.custom_attrs: dict[str, int | float | str] = {}

    # ── Derived stats (Week 7: @property) ────────────────────────────

    @property
    def speed(self) -> float:
        """Turn-order speed. Mirrors Character.speed interface."""
        return self.dexterity * 0.5 + self.speed_bonus

    @property
    def damage(self) -> float:
        """Base damage per hit."""
        return self.strength * 1.5 + self.dexterity * 0.5

    # ── Combat interface (mirrors Character) ─────────────────────────

    def take_damage(self, amount: float):
        """Week 2: if/else for HP floor."""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        if not self.is_alive():
            print(f"  {self.name} has been slain!")

    def is_alive(self) -> bool:
        return self.hp > 0

    def restore_full(self):
        self.hp = self.max_hp

    # ── ENGINE: custom attributes (Week 3: dict operations) ──────────

    def set_attr(self, key: str, value: int | float | str):
        """Add or update a custom attribute (ENGINE feature)."""
        self.custom_attrs[key] = value
        print(f"  [{self.name}] {key} = {value}")

    def get_attr(self, key: str, default=None):
        return self.custom_attrs.get(key, default)

    # ── Display ──────────────────────────────────────────────────────

    def show_stats(self):
        sep = "-" * 30
        print(sep)
        print(f"  {self.name}")                                     # Week 1: f-string
        print(f"  HP      : {self.hp} / {self.max_hp}")
        print(f"  Strength: {self.strength}")
        print(f"  Dexterity:{self.dexterity}")
        print(f"  Damage  : {self.damage:.1f}")
        print(f"  Speed   : {self.speed:.1f}")
        print(f"  XP drop : {self.xp_reward}")
        print(f"  Gold drop: {self.gold_reward}g")
        if self.description:
            print(f"  \"{self.description}\"")
        if self.custom_attrs:                                        # Week 3: dict iteration
            print("  Custom attrs:")
            for k, v in self.custom_attrs.items():
                print(f"    {k}: {v}")
        print(sep)

    def __repr__(self) -> str:                                       # Week 7: __repr__
        return f"Monster({self.name!r}, hp={self.hp}/{self.max_hp}, dmg={self.damage:.1f})"

    # ── Alternative constructor (Week 7: @classmethod) ───────────────

    @classmethod
    def from_dict(cls, data: dict) -> "Monster":
        m = cls(
            name        = data["name"],
            hp          = data.get("hp", 30),
            strength    = data.get("strength", 5),
            dexterity   = data.get("dexterity", 5),
            speed_bonus = data.get("speed_bonus", 0.0),
            xp_reward   = data.get("xp_reward", 20),
            gold_reward = data.get("gold_reward", 10),
            description = data.get("description", ""),
        )
        m.custom_attrs = data.get("custom_attrs", {})
        return m

    @classmethod
    def random_from_catalogue(cls) -> "Monster":
        """Pick a random monster from DEFAULT_MONSTERS (Week 3: list indexing)."""
        data = random.choice(DEFAULT_MONSTERS)
        return cls.from_dict(data)

    def to_dict(self) -> dict:
        return {
            "name":        self.name,
            "hp":          self.max_hp,
            "strength":    self.strength,
            "dexterity":   self.dexterity,
            "speed_bonus": self.speed_bonus,
            "xp_reward":   self.xp_reward,
            "gold_reward": self.gold_reward,
            "description": self.description,
            "custom_attrs": self.custom_attrs,
        }


# ── Inheritance: BossMonster (Week 7: inheritance, method override) ───────────

class BossMonster(Monster):
    """
    A tougher monster with a multi-phase rage mechanic.
    Demonstrates inheritance and method overriding (Week 7).
    """

    def __init__(self, name: str, hp: int = 200, strength: int = 18,
                 dexterity: int = 8, xp_reward: int = 200,
                 gold_reward: int = 100, description: str = "BOSS"):
        super().__init__(name, hp, strength, dexterity,
                         xp_reward=xp_reward, gold_reward=gold_reward,
                         description=description)
        self.enraged = False

    def take_damage(self, amount: float):
        """Override: trigger rage below 50% HP."""
        super().take_damage(amount)
        if self.is_alive() and not self.enraged and self.hp < self.max_hp * 0.5:
            self.enraged = True
            print(f"  *** {self.name} ENRAGES! Strength doubled! ***")
            self.strength *= 2

    def show_stats(self):
        super().show_stats()
        print(f"  [BOSS]  Enraged: {self.enraged}")


# ── ENGINE helper: build a monster interactively from user input ──────────────

def create_monster_interactive() -> Monster:
    """
    Week 1: input()
    Week 2: while + try/except for validation
    Week 5: function
    """
    print("\n  -- Create New Monster --")

    name = input("  Name: ").strip() or "Unknown"
    description = input("  Description (optional): ").strip()

    def ask_int(prompt: str, default: int) -> int:      # Week 5: nested function
        while True:                                       # Week 2: while loop
            raw = input(f"  {prompt} [{default}]: ").strip()
            if raw == "":
                return default
            try:
                val = int(raw)                           # Week 1: int conversion
                if val < 0:
                    raise ValueError("Must be >= 0")
                return val
            except ValueError as e:
                print(f"  Invalid: {e}. Try again.")

    hp         = ask_int("HP",          30)
    strength   = ask_int("Strength",    5)
    dexterity  = ask_int("Dexterity",   5)
    xp_reward  = ask_int("XP reward",   20)
    gold_reward= ask_int("Gold reward", 10)

    m = Monster(name, hp, strength, dexterity,
                xp_reward=xp_reward, gold_reward=gold_reward,
                description=description)

    # Optional custom attributes (Week 3: dict building)
    print("  Add custom attributes? (leave name blank to stop)")
    while True:                                          # Week 2: while loop
        attr_name = input("  Attr name: ").strip()
        if not attr_name:
            break
        attr_val = input(f"  {attr_name} value: ").strip()
        # Try int → float → str (Week 2: if/elif/else)
        try:
            m.set_attr(attr_name, int(attr_val))
        except ValueError:
            try:
                m.set_attr(attr_name, float(attr_val))
            except ValueError:
                m.set_attr(attr_name, attr_val)

    return m