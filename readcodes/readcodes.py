#!/usr/bin/env python3
"""Read codes from ShackNews HTML and 
"""
from pathlib import Path
from json import dump

# Pathing
cwd = Path(__file__).resolve().parent
root = cwd.parent
fncodes = root / 'codes.json'
fnhtml = cwd / 'All Stratagems & input codes - Helldivers 2 Shacknews.html'

# UTF-16 arrow keys
left = '\u2190'
down = '\u2193'
up = '\u2191'
right = '\u2192'
keydict = {left: 'LEFT', right: 'RIGHT', up: 'UP', down: 'DOWN'}


def striphtml(txt):
    """Stratagem info stored in tables. Return the relevant raw text."""
    txt = txt.strip()
    i1 = txt[:-1].rfind(';">') + 3  # start of entry
    i2 = txt.rfind('</td>')  # end of entry
    return txt[i1:i2]


def code2ducky(txt):
    """Convert UTF-16 arrow symbols to CAPSTEXT name for duckyscript,
        e.g. Takes left arrow symbol ('\u2190') and returns 'LEFT'.
    """
    txtout = [keydict[c] for c in txt]
    return ' '.join(txtout)


# Read HTML
with open(fnhtml, 'r') as f:
    lines = f.read().splitlines()

# Identify Stratagems
# - Table format goes "Name"\n"Code". Codes are easier to find, so
# - find the codes and then get the name from the previous line.
out = []
keys = list(keydict.keys())
for i, line in enumerate(lines):
    line, lineprev = lines[i], lines[i - 1]
    for k in keys:
        if k in line:
            code = striphtml(line)
            if not all([v in keys for v in code]):  # skip non-code HTML lines
                break
            name = striphtml(lines[i - 1])
            out.append({name: code2ducky(code)})
            break

# Save
with open(fncodes, 'w') as f:
    dump(out, f, indent=1)
