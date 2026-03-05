import json
from collections import Counter
from pathlib import Path

data_file = Path(__file__).parent.parent.parent / "data" / "output" / "final.json"
creatures = json.load(open(data_file))

colors_found = {}
for creature in creatures.values():
    colors = sorted(creature.get('colors', []))
    key = str(colors)
    colors_found[key] = colors_found.get(key, 0) + 1

print("Color distributions in creatures:\n")
for combo, count in sorted(colors_found.items(), key=lambda x: x[1], reverse=True):
    print(f"{combo}: {count}")
