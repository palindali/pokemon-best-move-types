# Script to calculate best move types to cover weaknesses of a certain Pokémon
import pandas as pd
from sys import argv, exit

cur_types = argv[1:] 

types = ['normal', 'fighting', 'flying', 'poison', 'ground', 'rock', 'bug', 
    'ghost', 'steel', 'fire', 'water', 'grass', 'electric', 'psychic', 'ice', 
    'dragon', 'dark', 'fairy']

if not all(t in types for t in cur_types):
    exit('types provided not in type list!')

# Pokémon attacking type chart
type_chart = pd.DataFrame({
    'normal':   [1, 1, 1, 1, 1,.5, 1, 0,.5, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'fighting': [2, 1,.5,.5, 1, 2,.5, 0, 2, 1, 1, 1, 1,.5, 2, 1, 2,.5],
    'flying':   [1, 2, 1, 1, 1,.5, 2, 1,.5, 1, 1, 2,.5, 1, 1, 1, 1, 1],
    'poison':   [1, 1, 1,.5,.5,.5, 1,.5, 0, 1, 1, 2, 1, 1, 1, 1, 1, 2],
    'ground':   [1, 1, 0, 2, 1, 2,.5, 1, 2, 2, 1,.5, 2, 1, 1, 1, 1, 1],
    'rock':     [1,.5, 2, 1,.5, 1, 2, 1,.5, 2, 1, 1, 1, 1, 2, 1, 1, 1],
    'bug':      [1,.5,.5,.5, 1, 1, 1,.5,.5,.5, 1, 2, 1, 2, 1, 1,.5, 1],
    'ghost':    [0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1,.5, 1],
    'steel':    [1, 1, 1, 1, 1, 2, 1, 1,.5,.5,.5, 1,.5, 1, 2, 1, 1, 2],
    'fire':     [1, 1, 1, 1, 1,.5, 2, 1, 2,.5,.5, 2, 1, 1, 2,.5, 1, 1],
    'water':    [1, 1, 1, 1, 2, 2, 1, 1, 1, 2,.5,.5, 1, 1, 1,.5, 1, 1],
    'grass':    [1, 1,.5,.5, 2, 2,.5, 1,.5,.5, 2,.5, 1, 1, 1,.5, 1, 1],
    'electric': [1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 2,.5,.5, 1, 1,.5, 1, 1],
    'psychic':  [1, 2, 1, 2, 1, 1, 1, 1,.5, 1, 1, 1, 1,.5, 1, 1, 0, 1],
    'ice':      [1, 1, 2, 1, 2, 1, 1, 1,.5,.5,.5, 2, 1, 1,.5, 2, 1, 1],
    'dragon':   [1, 1, 1, 1, 1, 1, 1, 1,.5, 1, 1, 1, 1, 1, 1, 2, 1, 0],
    'dark':     [1,.5, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1,.5,.5],
    'fairy':    [1, 2, 1,.5, 1, 1, 1, 1,.5,.5, 1, 1, 1, 1, 1, 2, 2, 1]
}, index=types).T

# Initial incoming attack multiplier
mult = pd.Series([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
    index=types)

# Get actual defense multipliers based on two types
for t in cur_types:
    mult = mult * type_chart[t]

print('Current typing defense multiplier list:')
print(mult)
    
# Get types that are strong against current Pokémon typing
supers = list(mult[mult > 1].index)

# Get types that are strong against the types that are strong against current
#  Pokémon typing
f_supers = {t:0 for t in types}
for super in supers:
    cur_f_supers = list(type_chart[super][type_chart[super] > 1].index)
    for s in cur_f_supers:
        f_supers[s] += 1
    # f_supers.extend(cur_f_supers)
f_supers = {k: v for k, v in sorted(f_supers.items(), key=lambda item: item[1], reverse=True) if v != 0}

print('Best coverage move types:')
print(pd.Series(f_supers))
