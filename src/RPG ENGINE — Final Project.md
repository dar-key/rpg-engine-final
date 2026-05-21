RPG ENGINE — Final Project
==========================
Authors: Abilmansur + Sergey
Python 3.10+

HOW TO RUN
----------
1. Make sure all .py files are in the same folder:
   main.py, character.py, items.py, shop.py,
   monster.py, combat.py, dungeon.py, save.py

2. Run:
   python main.py

3. A 'saves/' folder will be created automatically when you save.

FILES
-----
main.py       — Entry point, main menu
character.py  — Character class, stats, inventory, equip
items.py      — Item class, default item catalogue
shop.py       — Shop: buy/sell, ENGINE item editor
monster.py    — Monster class, default monsters, ENGINE monster creator
combat.py     — Turn-based combat loop
dungeon.py    — Dungeon rooms, room types, ENGINE dungeon configurator
save.py       — JSON save/load (saves/savegame.json)

ENGINE FEATURES (marked [ENGINE] in menus)
-------------------------------------------
- Add/remove/edit items in shop at runtime
- Create custom monsters with any attributes
- Configure dungeon: name, room count, difficulty, monster pool
- Change character speed formula (default / agile / slow)

No external libraries required — only Python standard library.