import json
import random
from pathlib import Path

# Load creatures
data_file = Path(__file__).parent.parent.parent / "data" / "output" / "final.json"
with open(data_file) as f:
    creatures = json.load(f)

print(f"✓ Loaded {len(creatures)} creatures from final.json\n")

# Test 1: Guild color mapping
print("=== Test 1: Guild Color Distribution ===")
guild_creatures = {
    'azorius': [], 'dimir': [], 'rakdos': [], 'golgari': [],
    'selesnya': [], 'orzhov': [], 'izzet': [], 'gruul': [],
    'boros': [], 'simic': []
}

color_to_guild = {
    ('U', 'W'): 'azorius', ('B', 'U'): 'dimir', ('B', 'R'): 'rakdos', 
    ('B', 'G'): 'golgari', ('G', 'W'): 'selesnya', ('B', 'W'): 'orzhov', 
    ('R', 'U'): 'izzet', ('G', 'R'): 'gruul', ('R', 'W'): 'boros', ('G', 'U'): 'simic'
}

for creature in creatures.values():
    colors = creature.get('colors', [])
    if len(colors) == 2:
        sorted_colors = tuple(sorted(colors))
        guild = color_to_guild.get(sorted_colors)
        if guild:
            guild_creatures[guild].append({
                'name': creature.get('name', '?'),
                'cr': creature.get('Challenge', '?').split()[0] if creature.get('Challenge') else '?',
                'traits': len(creature.get('Traits', '')) > 0
            })

for guild, creatures_list in sorted(guild_creatures.items()):
    avg_cr = 'N/A'
    if creatures_list:
        crs = []
        for c in creatures_list:
            try:
                crs.append(float(c['cr']))
            except:
                pass
        if crs:
            avg_cr = f"{sum(crs)/len(crs):.1f}"
    
    traits_with = sum(1 for c in creatures_list if c['traits'])
    print(f"  {guild.ljust(10)}: {len(creatures_list):3} creatures | Avg CR: {str(avg_cr).ljust(4)} | With traits: {traits_with}")

print(f"\nTotal creatures by guild: {sum(len(c) for c in guild_creatures.values())}")

# Test 2: CR distribution
print("\n=== Test 2: CR Distribution ===")
cr_distribution = {}
for creature in creatures.values():
    challenge = creature.get('Challenge', '0')
    cr = challenge.split()[0] if challenge else '0'
    cr_distribution[cr] = cr_distribution.get(cr, 0) + 1

for cr in sorted(cr_distribution.keys(), key=lambda x: float(x.replace('/', '.')) if '/' in x else float(x)):
    count = cr_distribution[cr]
    bar = '█' * min(count // 5, 50)
    print(f"  CR {cr:3} {'(':3} {count:3} {bar}")

# Test 3: Sample encounter simulation
print("\n=== Test 3: Sample Encounter Generation ===")
selected_guild = random.choice(list(guild_creatures.keys()))
selected_guild_creatures = guild_creatures[selected_guild]

if selected_guild_creatures:
    encounter = random.sample(selected_guild_creatures, min(3, len(selected_guild_creatures)))
    total_xp = 0
    
    xp_values = {
        '0': 10, '1/8': 25, '1/4': 50, '1/2': 100, '1': 200, '2': 450, 
        '3': 700, '4': 1100, '5': 1800, '6': 2300, '7': 2900, '8': 3900,
        '9': 5000, '10': 5900, '15': 13000, '20': 25000
    }
    
    print(f"\n  Guild: {selected_guild.upper()}")
    print(f"  Creatures:")
    for creature in encounter:
        xp = xp_values.get(creature['cr'], 0)
        total_xp += xp
        print(f"    • {creature['name']:30} (CR {creature['cr']}, {xp} XP)")
    
    print(f"\n  Total XP: {total_xp} (Difficulty: {'Easy' if total_xp < 300 else 'Medium' if total_xp < 600 else 'Hard'})")
else:
    print(f"  No creatures found for guild {selected_guild}")

print("\n✓ All tests completed successfully!")
