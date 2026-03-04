import json
from collections import Counter

creatures = json.load(open('final.json'))

colors_found = {}
for creature in creatures.values():
    colors = sorted(creature.get('colors', []))
    key = str(colors)
    colors_found[key] = colors_found.get(key, 0) + 1

print("Color distributions in creatures:\n")
for combo, count in sorted(colors_found.items(), key=lambda x: x[1], reverse=True):
    print(f"{combo}: {count}")
