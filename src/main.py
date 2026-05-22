import sys
import io
from character import Character
from shop import Shop
from monster import Monster, DEFAULT_MONSTERS, prompt_new_monster
from dungeon import Dungeon, prompt_new_dungeon
from save import save_game, load_game, save_exists, delete_save
from utils import *

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

player_loaded = False
player: Character
shop: Shop
monsters: list[Monster] = list(DEFAULT_MONSTERS)


def _require_player() -> bool:
    if not player_loaded:
        print("  No character loaded. Create or load one first.")
        return False
    return True


def create_character():
    clear_screen()
    global player, player_loaded
    print("\n  -- Create Character --")
    name = input("  Name: ").strip()
    if not name:
        print("  Name cannot be empty.")
        return

    print("  Distribute 15 stat points across STR / DEX / INT (min 1 each).")
    try:
        str_ = int(input("  Strength  (e.g. 7): "))
        dex = int(input("  Dexterity (e.g. 5): "))
        int_ = int(input("  Intellect (e.g. 3): "))
    except ValueError:
        print("  Invalid input. Using defaults (5/5/5).")
        str_, dex, int_ = 5, 5, 5

    total = str_ + dex + int_
    if total != 15 or min(str_, dex, int_) < 1:
        print(f"  Stats must sum to 15, each at least 1. Got {total}. Using defaults.")
        str_, dex, int_ = 5, 5, 5

    player = Character(
        name=name, strength=str_, dexterity=dex, intelligence=int_, hp=100, gold=50
    )
    print(f"\n  Character '{player.name}' created!")
    clear_screen()
    player.show_stats()
    player_loaded = True


def character_menu():
    if not _require_player():
        return
    clear_screen()
    while True:
        print_divider()
        print("  CHARACTER MENU")
        print("  1. View stats")
        print("  2. View inventory")
        print("  3. Equip item")
        print("  4. Unequip slot")
        print("  5. Change speed formula  [ENGINE]")
        print("  0. Back")
        choice = input("  > ").strip()

        if choice == "1":
            player.show_stats()

        elif choice == "2":
            player.show_inventory()

        elif choice == "3":
            player.show_inventory()
            if player.inventory:
                try:
                    idx = int(input("  Equip item #: ")) - 1
                    if 0 <= idx < len(player.inventory):
                        player.equip(player.inventory[idx])
                    else:
                        print("  Invalid number.")
                except ValueError:
                    print("  Please enter a number.")

        elif choice == "4":
            slot = input("  Slot to unequip (weapon/armor): ").strip().lower()
            player.unequip(slot)

        elif choice == "5":
            print(f"  Formulas: {list(Character.SPEED_FORMULAS.keys())}")
            f = input("  Choose formula: ").strip()
            player.set_speed_formula(f)

        elif choice == "0":
            break

        clear_screen()


def monster_menu():
    clear_screen()

    while True:
        print_divider()
        print("  MONSTER REGISTRY  [ENGINE]")
        print("  1. List all monsters")
        print("  2. View monster details")
        print("  3. Create new monster")
        print("  0. Back")
        choice = input("  > ").strip()

        if choice == "1":
            print()
            for i, m in enumerate(monsters, 1):
                print(
                    f"  {i:2}. {m.name:<20} HP:{m.max_hp}  STR:{m.strength}  DEX:{m.dexterity}"
                )

        elif choice == "2":
            for i, m in enumerate(monsters, 1):
                print(f"  {i}. {m.name}")
            try:
                idx = int(input("  Monster #: ")) - 1
                if 0 <= idx < len(monsters):
                    monsters[idx].show_stats()
                else:
                    print("  Invalid number.")
            except ValueError:
                print("  Please enter a number.")

        elif choice == "3":
            m = prompt_new_monster()
            if m:
                monsters.append(m)
                print(f"  '{m.name}' added to registry.")

        elif choice == "0":
            break

        clear_screen()


def dungeon_menu():
    if not _require_player():
        return
    print_divider()
    print("  DUNGEON")
    print("  1. Quick dungeon (default settings)")
    print("  2. Custom dungeon  [ENGINE]")
    print("  0. Back")
    choice = input("  > ").strip()

    if choice == "1":
        dungeon = Dungeon(dungeon_level=player.level)
        dungeon.enter(player)

    elif choice == "2":
        dungeon = prompt_new_dungeon(monsters)
        if dungeon:
            dungeon.enter(player)


def quick_fight():
    clear_screen()
    if not _require_player():
        return
    print("\n  Quick Fight — choose an opponent:")
    for i, m in enumerate(monsters, 1):
        print(f"  {i}. {m.name}")
    try:
        idx = int(input("  Monster #: ")) - 1
        if not (0 <= idx < len(monsters)):
            print("  Invalid number.")
            return
    except ValueError:
        print("  Please enter a number.")
        return

    from combat import run_combat

    run_combat(player, monsters[idx].clone())


def save_menu():
    clear_screen()
    global player, shop
    print_divider()
    print("  SAVE / LOAD")
    print("  1. Save game")
    print("  2. Load game")
    print("  3. Delete save")
    print("  0. Back")
    choice = input("  > ").strip()

    if choice == "1":
        if not _require_player():
            return
        save_game(player, shop)

    elif choice == "2":
        result = load_game()
        if result:
            player, shop = result
            print(f"  Loaded character: {player.name}  (Level {player.level})")

    elif choice == "3":
        confirm = input("  Are you sure? (yes/no): ").strip().lower()
        if confirm == "yes":
            delete_save()

    clear_screen()


def main():
    global player, shop, player_loaded

    shop = Shop()

    print_banner()

    if save_exists():
        print("\n  A save file was found.")
        ans = input("  Load it? (y/n): ").strip().lower()
        if ans != "n":
            result = load_game()
            if result:
                player, shop = result
                player_loaded = True

    while True:
        print_divider()
        char_line = (
            f"  [{player.name}  Lv.{player.level}  {player.hp:.1f}HP  {player.gold}g]"
            if player_loaded
            else "  [No character]"
        )
        print(char_line)
        print()
        print("  MAIN MENU")
        print("  1. Create character")
        print("  2. Character & inventory")
        print("  3. Shop")
        print("  4. Quick fight")
        print("  5. Enter dungeon")
        print("  6. Monster registry  [ENGINE]")
        print("  7. Save / Load")
        print("  0. Quit")
        print()

        choice = input("  > ").strip()

        if choice == "1":
            create_character()

        elif choice == "2":
            character_menu()

        elif choice == "3":
            if _require_player():
                shop.open(player)

        elif choice == "4":
            quick_fight()

        elif choice == "5":
            dungeon_menu()

        elif choice == "6":
            monster_menu()

        elif choice == "7":
            save_menu()

        elif choice == "0":
            if player:
                ans = input("  Save before quitting? (y/n): ").strip().lower()
                if ans != "n":
                    save_game(player, shop)
            print("\n  Goodbye!\n")
            break

        else:
            print("  Unknown option.")


if __name__ == "__main__":
    main()
