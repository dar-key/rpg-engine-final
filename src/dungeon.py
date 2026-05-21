from __future__ import annotations
import random
from typing import TYPE_CHECKING

from monster import Monster, DEFAULT_MONSTERS
from combat import run_combat

if TYPE_CHECKING:
    from character import Character
ROOM_TYPES = ("combat", "combat", "combat", "treasure", "rest", "trap", "boss")


class Room:
    def __init__(self, room_type: str, monster: Monster | None = None, gold_reward: int = 0):
        self.room_type   = room_type
        self.monster     = monster
        self.gold_reward = gold_reward
        self.cleared     = False

    def describe(self):
        icons = {
            "combat":   "⚔",
            "treasure": "💰",
            "rest":     "🏕",
            "trap":     "⚡",
            "boss":     "💀",
        }
        icon = icons.get(self.room_type, "?")
        print(f"  {icon}  Room type: {self.room_type.upper()}", end="")
        if self.monster:
            print(f"  — {self.monster.name} lurks here!", end="")
        print()


class Dungeon:
    def __init__(
        self,
        name: str = "Dark Dungeon",
        num_rooms: int = 5,
        monster_pool: list[Monster] | None = None,
        boss: Monster | None = None,
        dungeon_level: int = 1,
    ):
        self.name          = name
        self.dungeon_level = max(1, dungeon_level)
        self.current_room  = 0
        self.monster_pool  = monster_pool or list(DEFAULT_MONSTERS[:-1])  
        self.boss          = boss or DEFAULT_MONSTERS[-1].clone()          
        self.rooms         = self._generate(num_rooms)


    def _scale(self, monster: Monster) -> Monster:
        m = monster.clone()
        scale = self.dungeon_level
        m.max_hp    = int(m.max_hp    * (1 + 0.3 * (scale - 1)))
        m.hp        = m.max_hp
        m.strength  = int(m.strength  * (1 + 0.2 * (scale - 1)))
        m.dexterity = int(m.dexterity * (1 + 0.1 * (scale - 1)))
        m.xp_reward = int(m.xp_reward * scale)
        m.gold_reward = int(m.gold_reward * scale)
        return m

    def _generate(self, num_rooms: int) -> list[Room]:
        rooms: list[Room] = []
        for i in range(num_rooms):
            is_last = (i == num_rooms - 1)
            if is_last:
                boss = self._scale(self.boss)
                rooms.append(Room("boss", monster=boss))
            else:
                rtype = random.choice(ROOM_TYPES[:-1])  
                if rtype == "combat":
                    template = random.choice(self.monster_pool)
                    rooms.append(Room("combat", monster=self._scale(template)))
                elif rtype == "treasure":
                    gold = random.randint(10, 30) * self.dungeon_level
                    rooms.append(Room("treasure", gold_reward=gold))
                elif rtype == "rest":
                    rooms.append(Room("rest"))
                elif rtype == "trap":
                    rooms.append(Room("trap"))
        return rooms


    @property
    def completed(self) -> bool:
        return self.current_room >= len(self.rooms)

    @property
    def room(self) -> Room | None:
        if self.completed:
            return None
        return self.rooms[self.current_room]


    def show_map(self):
        print(f"\n  === {self.name.upper()} (Level {self.dungeon_level}) ===")
        print(f"  Rooms: {len(self.rooms)}  |  Current: {self.current_room + 1}")
        for i, r in enumerate(self.rooms):
            marker = ">>>" if i == self.current_room else "   "
            cleared = "[X]" if r.cleared else "[ ]"
            print(f"  {marker} {cleared} Room {i+1}: {r.room_type.upper()}", end="")
            if r.monster and not r.cleared:
                print(f" ({r.monster.name})", end="")
            print()


    def _resolve_combat(self, character: "Character", room: Room) -> bool:
        result = run_combat(character, room.monster)
        if not result.victory and character.is_alive():
            print("  You fled! The dungeon awaits…")
            return True
        return character.is_alive()

    def _resolve_treasure(self, character: "Character", room: Room):
        print(f"\n  💰 You found a treasure chest! +{room.gold_reward}g")
        character.earn_gold(room.gold_reward)

    def _resolve_rest(self, character: "Character"):
        heal_amount = character.max_hp_total * 0.4
        old = character.hp
        character.heal(heal_amount)
        print(f"\n  🏕 A rest site. You recover {character.hp - old:.0f} HP. "
              f"({character.hp:.0f}/{character.max_hp_total})")

    def _resolve_trap(self, character: "Character"):
        dmg = random.randint(5, 15) * self.dungeon_level
        print(f"\n  ⚡ TRAP! You take {dmg} damage!")
        character.take_damage(dmg)

    def enter(self, character: "Character") -> bool:
        print("\n" + "=" * 40)
        print(f"  Entering: {self.name}  (Level {self.dungeon_level})")
        print("=" * 40)

        while not self.completed:
            room = self.room
            self.show_map()
            print()
            room.describe()

            if room.room_type in ("combat", "boss"):
                alive = self._resolve_combat(character, room)
                if not alive:
                    print("\n  You have perished in the dungeon.")
                    return False
                if not character.is_alive():
                    return False

            elif room.room_type == "treasure":
                self._resolve_treasure(character, room)

            elif room.room_type == "rest":
                self._resolve_rest(character)

            elif room.room_type == "trap":
                self._resolve_trap(character)
                if not character.is_alive():
                    print("\n  You have perished in the dungeon.")
                    return False

            room.cleared = True
            self.current_room += 1

            if not self.completed:
                cont = input("\n  Continue to next room? (y/n): ").strip().lower()
                if cont != "y":
                    print("  You retreat from the dungeon.")
                    return False

        print("\n" + "=" * 40)
        print(f"  🏆 DUNGEON CLEARED: {self.name}!")
        print("=" * 40)
        return True



def prompt_new_dungeon(available_monsters: list[Monster]) -> "Dungeon | None":
    print("\n  -- Configure Dungeon --")
    try:
        name   = input("  Dungeon name (Enter for 'Dark Dungeon'): ").strip() or "Dark Dungeon"
        rooms  = int(input("  Number of rooms (3-10): "))
        rooms  = max(3, min(rooms, 10))
        level  = int(input("  Dungeon level / difficulty (1-5): "))
        level  = max(1, min(level, 5))

        print("\n  Available monsters for pool:")
        for i, m in enumerate(available_monsters, 1):
            print(f"    {i}. {m.name}")
        raw = input("  Pick monsters for pool (comma-separated numbers, or Enter for all): ").strip()
        if raw:
            indices = [int(x) - 1 for x in raw.split(",") if x.strip().isdigit()]
            pool = [available_monsters[i] for i in indices if 0 <= i < len(available_monsters)]
        else:
            pool = available_monsters

        return Dungeon(name=name, num_rooms=rooms, monster_pool=pool, dungeon_level=level)

    except ValueError as e:
        print(f"  Error: {e}")
        return None