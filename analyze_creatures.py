import json

with open('final.json') as f:
    creatures = json.load(f)

# Sample creatures with their data
creatures_list = list(creatures.values())[:5]
for c in creatures_list:
    name = c.get('name', '?')
    challenge = c.get('Challenge', '?').split()[0]
    traits_len = len(c.get('Traits', ''))
    colors = c.get('colors', [])
    print(f"{name:25} CR={challenge:2} Traits={traits_len:4} colors={colors}")

print(f"\nTotal creatures: {len(creatures)}")
print(f"Sample creature has keys: {list(list(creatures.values())[0].keys())[:10]}")
