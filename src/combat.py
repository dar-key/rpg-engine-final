from __future__ import annotations
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from character import Character
    from monster import Monster


class CombatResult:
    def __init__(self, victory: bool, xp: int = 0, gold: int = 0):
        self.victory  = victory
        self.xp_gained   = xp
        self.gold_gained = gold


def _build_turn_order(character: "Character", monster: "Monster") -> list:
    combatants = [
        (character.speed + random.uniform(0, 0.1), character),
        (monster.speed   + random.uniform(0, 0.1), monster),
    ]
    combatants.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in combatants]


def _use_potion(character: "Character") -> bool:
    potions = [(i, item) for i, item in enumerate(character.inventory)
               if item.item_type == "potion"]
    if not potions:
        print("  You have no potions.")
        return False

    print("  Available potions:")
    for idx, (inv_idx, item) in enumerate(potions, 1):
        print(f"    {idx}. {item.name}  (HP +{item.hp_effect})")

    try:
        choice = int(input("  Use potion #: ")) - 1
        if not (0 <= choice < len(potions)):
            print("  Invalid choice.")
            return False
    except ValueError:
        print("  Invalid input.")
        return False

    inv_idx, potion = potions[choice]
    old_hp = character.hp
    character.heal(potion.hp_effect)
    character.remove_item(potion)
    healed = character.hp - old_hp
    print(f"  Used {potion.name}. Restored {healed:.0f} HP. "
          f"({character.hp:.0f}/{character.max_hp_total})")
    return True


def run_combat(character: "Character", monster: "Monster") -> CombatResult:
    print("\n" + "=" * 40)
    print(f"  ⚔  COMBAT: {character.name}  vs  {monster.name}  ⚔")
    print("=" * 40)
    monster.show_stats()

    round_num = 0

    while character.is_alive() and monster.is_alive():
        round_num += 1
        print(f"\n  -- Round {round_num} --")
        print(f"  {character.name}: {character.hp:.0f}/{character.max_hp_total} HP  |  "
              f"{monster.name}: {monster.hp:.0f}/{monster.max_hp} HP")

        turn_order = _build_turn_order(character, monster)

        for combatant in turn_order:
            if not character.is_alive() or not monster.is_alive():
                break

            if combatant is character:
                print(f"\n  Your turn! (Speed: {character.speed:.1f})")
                print("    1. Attack")
                print("    2. Use Potion")
                print("    3. Flee")

                action = input("  > ").strip()

                if action == "1":
                    dmg = character.damage * random.uniform(0.9, 1.1)
                    monster.take_damage(dmg)
                    print(f"  {character.name} attacks {monster.name} for {dmg:.1f} damage!")

                elif action == "2":
                    used = _use_potion(character)
                    if not used:
                        dmg = character.damage * random.uniform(0.9, 1.1)
                        monster.take_damage(dmg)
                        print(f"  {character.name} attacks for {dmg:.1f} (no potion used).")

                elif action == "3":
                    flee_chance = 0.4 + max(0, (character.speed - monster.speed) * 0.02)
                    flee_chance = min(flee_chance, 0.9)
                    if random.random() < flee_chance:
                        print(f"  {character.name} fled from battle!")
                        return CombatResult(victory=False)
                    else:
                        print("  Failed to flee!")

                else:
                    dmg = character.damage * random.uniform(0.9, 1.1)
                    monster.take_damage(dmg)
                    print(f"  {character.name} attacks for {dmg:.1f}.")

            else:
                dmg = monster.damage * random.uniform(0.85, 1.15)
                character.take_damage(dmg)
                print(f"  {monster.name} attacks {character.name} for {dmg:.1f} damage!")

    print("\n" + "=" * 40)
    if character.is_alive():
        print(f"  VICTORY! {character.name} defeated {monster.name}!")
        print(f"  Gained: {monster.xp_reward} XP  |  {monster.gold_reward}g")
        print("=" * 40)
        character.gain_experience(monster.xp_reward)
        character.earn_gold(monster.gold_reward)
        return CombatResult(victory=True, xp=monster.xp_reward, gold=monster.gold_reward)
    else:
        print(f"  DEFEAT. {character.name} was slain by {monster.name}.")
        print("=" * 40)
        return CombatResult(victory=False)