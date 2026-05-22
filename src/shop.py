from item import Item, DEFAULT_ITEMS
from typing import TYPE_CHECKING
from utils import clear_screen

if TYPE_CHECKING:
    from character import Character


class Shop:

    DEFAULT_SELL_RATE = 0.5

    def __init__(self, items: list[Item] | None = None, sell_rate: float | None = None):
        self.catalogue: list[Item] = items if items is not None else list(DEFAULT_ITEMS)
        self.sell_rate: float = (
            sell_rate if sell_rate is not None else self.DEFAULT_SELL_RATE
        )

    def show_catalogue(self):
        if not self.catalogue:
            print("  The shop is empty.")
            return
        print("=" * 40)
        print("  SHOP CATALOGUE")
        print("=" * 40)
        for i, item in enumerate(self.catalogue, 1):
            effects = []
            if item.attack_effect:
                effects.append(f"ATK+{item.attack_effect}")
            if item.hp_effect:
                effects.append(f"HP+{item.hp_effect}")
            if item.speed_effect:
                sign = "+" if item.speed_effect > 0 else ""
                effects.append(f"SPD{sign}{item.speed_effect}")
            fx_str = f"  [{', '.join(effects)}]" if effects else ""
            print(
                f"  {i:2}. {item.name:<20} {item.price:>4}g  "
                f"({item.rarity}){fx_str}"
            )
        print("=" * 40)
        print(f"  Sell rate: {int(self.sell_rate * 100)}% of item price")
        print("=" * 40)

    def buy(self, character: "Character", item_index: int) -> bool:
        if not (1 <= item_index <= len(self.catalogue)):
            print("  Invalid item number.")
            return False

        item = self.catalogue[item_index - 1]

        if not character.can_afford(item.price):
            print(f"  Not enough gold. Need {item.price}g, have {character.gold}g.")
            return False

        character.spend_gold(item.price)
        character.add_item(item)
        print(
            f"  Bought: {item.name} for {item.price}g. "
            f"Remaining gold: {character.gold}g."
        )
        return True

    def sell(self, character: "Character", inventory_index: int) -> bool:
        if not character.inventory:
            print("  Your inventory is empty.")
            return False

        if not (1 <= inventory_index <= len(character.inventory)):
            print("  Invalid inventory slot.")
            return False

        item = character.inventory[inventory_index - 1]
        sell_price = max(1, int(item.price * self.sell_rate))

        character.remove_item(item)
        character.earn_gold(sell_price)
        print(
            f"  Sold: {item.name} for {sell_price}g. " f"Total gold: {character.gold}g."
        )
        return True

    def add_item(self, item: Item):
        self.catalogue.append(item)
        print(f"  Added to shop: {item.name}")

    def remove_item(self, index: int) -> bool:
        if not (1 <= index <= len(self.catalogue)):
            print("  Invalid index.")
            return False
        removed = self.catalogue.pop(index - 1)
        print(f"  Removed from shop: {removed.name}")
        return True

    def edit_item_price(self, index: int, new_price: int) -> bool:
        if not (1 <= index <= len(self.catalogue)):
            print("  Invalid index.")
            return False
        item = self.catalogue[index - 1]
        old = item.price
        item.price = max(0, new_price)
        print(f"  {item.name}: price changed {old}g → {item.price}g")
        return True

    def set_sell_rate(self, rate: float):
        if not (0.0 <= rate <= 1.0):
            print("  Rate must be between 0.0 and 1.0")
            return
        self.sell_rate = rate
        print(f"  Sell rate updated to {int(rate * 100)}%")

    def open(self, character: "Character"):
        while True:
            clear_screen()

            print("\n--- SHOP ---")
            print("  1. Browse catalogue")
            print("  2. Buy item")
            print("  3. Sell item")
            print("  4. [ENGINE] Add item to shop")
            print("  5. [ENGINE] Remove item from shop")
            print("  6. [ENGINE] Edit item price")
            print("  7. [ENGINE] Change sell rate")
            print("  0. Leave shop")

            choice = input("  > ").strip()

            if choice == "1":
                self.show_catalogue()
            elif choice == "2":
                self.show_catalogue()
                character.show_inventory()
                try:
                    idx = int(input("  Buy item #: "))
                    self.buy(character, idx)
                except ValueError:
                    print("  Please enter a number.")
            elif choice == "3":
                character.show_inventory()
                try:
                    idx = int(input("  Sell item #: "))
                    self.sell(character, idx)
                except ValueError:
                    print("  Please enter a number.")
            elif choice == "4":
                item = _prompt_new_item()
                if item:
                    self.add_item(item)
            elif choice == "5":
                self.show_catalogue()
                try:
                    idx = int(input("  Remove item #: "))
                    self.remove_item(idx)
                except ValueError:
                    print("  Please enter a number.")
            elif choice == "6":
                self.show_catalogue()
                try:
                    idx = int(input("  Edit item #: "))
                    price = int(input("  New price: "))
                    self.edit_item_price(idx, price)
                except ValueError:
                    print("  Please enter numbers.")
            elif choice == "7":
                try:
                    rate = float(input("  New sell rate (0.0 – 1.0): "))
                    self.set_sell_rate(rate)
                except ValueError:
                    print("  Please enter a decimal number.")
            elif choice == "0":
                print("  Leaving shop.")
                break
            else:
                print("  Unknown option.")

    def to_dict(self) -> dict:
        return {
            "sell_rate": self.sell_rate,
            "catalogue": [item.to_dict() for item in self.catalogue],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Shop":
        items = [Item.from_dict(i) for i in data.get("catalogue", [])]
        return cls(items=items, sell_rate=data.get("sell_rate", cls.DEFAULT_SELL_RATE))


def _prompt_new_item() -> Item | None:

    print("\n  -- Create New Item --")
    try:
        name = input("  Name: ").strip()
        itype = input("  Type (weapon / armor / potion): ").strip().lower()
        price = int(input("  Price (gold): "))
        rarity = (
            input("  Rarity (common/uncommon/rare/epic/legendary): ").strip().lower()
        )
        desc = input("  Description: ").strip()
        atk = int(input("  Attack effect (0 if none): "))
        hp = int(input("  HP effect (0 if none): "))
        spd = int(input("  Speed effect (0 if none): "))
        return Item(name, itype, price, desc, rarity, atk, hp, spd)
    except ValueError as e:
        print(f"  Error creating item: {e}")
        return None
