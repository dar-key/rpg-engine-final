from character import Character
from item import Item
Bob = Character("bob", 10, 10, 10, 20, 100)
Axe = Item("axe", 10, "rare", "weapon", 100, "asdd")
Bob.show_stats()
Bob.take_damage(30)
Axe.show_item()