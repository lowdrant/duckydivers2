#!/usr/bin/env python3
"""Generate rubber ducky scripts from codes.json and keybinds.json"""
from itertools import tee
from json import load
from pathlib import Path


def genducky(name, code, keybinds):
    """Generate ducky script text file for stratagem"""
    out = []
    delay = keybinds['DELAY']
    ctrl = keybinds['CTRL']
    # preamble
    out.append(f'REM {name} Stratagem')
    # generate code
    out.append(f'HOLD {ctrl}')
    for c in code.split(' '):
        key = keybinds[c]
        out.append(f'DELAY {delay}')
        out.append(f'HOLD {key}')
        out.append(f'DELAY {delay}')
        out.append(f'RELEASE {key}')
    out.append(f'RELEASE {ctrl}')
    return '\n'.join(out)


# Pathing
root = Path(__file__).resolve().parent
fncodes = root / 'codes.json'
fnkeys = root / 'keybinds.json'
scriptdir = root / 'scripts'
if not scriptdir.exists():
    scriptdir.mkdir()

# Load Configuration
with open(fncodes, 'r') as f:
    codes = load(f)
with open(fnkeys, 'r') as f:
    keybinds = load(f)

# Generate DuckyScript
for n, c in codes.items():
    c = c.upper()  # enforce uppercase
    script = genducky(n, c, keybinds)
    with open(scriptdir / (n + '.txt'), 'w') as f:
        f.write(script)
