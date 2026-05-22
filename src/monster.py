class Monster:
    SPEED_FORMULAS = {
        "default": lambda dex, bonus: dex * 0.5 + bonus,
        "agile": lambda dex, bonus: dex * 1.0 + bonus,
        "slow": lambda dex, bonus: dex * 0.25 + bonus,
    }

    def __init__(
        self,
        name: str,
        hp: int = 30,
        strength: int = 5,
        dexterity: int = 5,
        xp_reward: int = 20,
        gold_reward: int = 10,
        speed_formula: str = "default",
        custom_attrs: dict | None = None,
    ):
        self.name = name
        self.max_hp = max(1, hp)
        self.hp = self.max_hp
        self.strength = strength
        self.dexterity = dexterity
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.speed_formula = (
            speed_formula if speed_formula in self.SPEED_FORMULAS else "default"
        )
        self.custom_attrs: dict = custom_attrs or {}

    @property
    def speed(self) -> float:
        fn = self.SPEED_FORMULAS.get(self.speed_formula, self.SPEED_FORMULAS["default"])
        return fn(self.dexterity, 0)

    @property
    def damage(self) -> float:
        return self.strength * 1.5 + self.dexterity * 0.5

    def take_damage(self, amount: float):
        self.hp = max(0, self.hp - amount)
        if not self.is_alive():
            print(f"  {self.name} has been slain!")

    def is_alive(self) -> bool:
        return self.hp > 0

    def heal(self, amount: float):
        self.hp = min(self.hp + amount, self.max_hp)

    def restore_full(self):
        self.hp = self.max_hp

    def show_stats(self):
        sep = "-" * 32
        print(sep)
        print(f"  {self.name}")
        print(sep)
        print(f"  HP       : {self.hp} / {self.max_hp}")
        print(f"  Strength : {self.strength}")
        print(f"  Dexterity: {self.dexterity}")
        print(f"  Damage   : {self.damage:.1f}")
        print(f"  Speed    : {self.speed:.1f}  ({self.speed_formula})")
        print(f"  XP drop  : {self.xp_reward}")
        print(f"  Gold drop: {self.gold_reward}g")
        if self.custom_attrs:
            print("  Custom attributes:")
            for k, v in self.custom_attrs.items():
                print(f"    {k}: {v}")
        print(sep)

    def set_attr(self, key: str, value):
        self.custom_attrs[key] = value
        print(f"  {self.name}.{key} = {value}")

    def get_attr(self, key: str, default=None):
        return self.custom_attrs.get(key, default)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "strength": self.strength,
            "dexterity": self.dexterity,
            "xp_reward": self.xp_reward,
            "gold_reward": self.gold_reward,
            "speed_formula": self.speed_formula,
            "custom_attrs": self.custom_attrs,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Monster":
        m = cls(
            name=data["name"],
            hp=data["max_hp"],
            strength=data["strength"],
            dexterity=data["dexterity"],
            xp_reward=data.get("xp_reward", 20),
            gold_reward=data.get("gold_reward", 10),
            speed_formula=data.get("speed_formula", "default"),
            custom_attrs=data.get("custom_attrs", {}),
        )
        m.hp = data.get("hp", m.max_hp)
        return m

    def clone(self) -> "Monster":
        m = Monster.from_dict(self.to_dict())
        m.restore_full()
        return m


DEFAULT_MONSTERS: list[Monster] = [
    Monster("Slime", hp=20, strength=3, dexterity=2, xp_reward=10, gold_reward=5),
    Monster("Goblin", hp=35, strength=6, dexterity=8, xp_reward=20, gold_reward=10),
    Monster(
        "Orc Warrior", hp=60, strength=12, dexterity=4, xp_reward=40, gold_reward=25
    ),
    Monster(
        "Dark Mage",
        hp=70,
        strength=15,
        dexterity=6,
        xp_reward=50,
        gold_reward=30,
        custom_attrs={"element": "dark", "spell_power": 10},
    ),
    Monster(
        "Dragon",
        hp=150,
        strength=25,
        dexterity=10,
        xp_reward=200,
        gold_reward=100,
        speed_formula="agile",
    ),
]


def prompt_new_monster() -> "Monster | None":
    print("\n  -- Create New Monster --")
    try:
        name = input("  Name: ").strip()
        hp = int(input("  HP: "))
        str_ = int(input("  Strength: "))
        dex = int(input("  Dexterity: "))
        xp = int(input("  XP reward: "))
        gold = int(input("  Gold reward: "))
        formula = input("  Speed formula (default/agile/slow): ").strip() or "default"

        monster = Monster(name, hp, str_, dex, xp, gold, formula)

        while True:
            more = input("  Add custom attribute? (y/n): ").strip().lower()
            if more != "y":
                break
            key = input("    Attribute name: ").strip()
            val = input("    Value: ").strip()
            try:
                val = int(val)
            except ValueError:
                try:
                    val = float(val)
                except ValueError:
                    pass
            monster.set_attr(key, val)

        print(f"  Monster '{monster.name}' created!")
        return monster

    except ValueError as e:
        print(f"  Error: {e}")
        return None
