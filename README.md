# duckydivers
DuckyScripts for calling in stratagems in HellDivers 2.

## Updating Code or Keybinds
To change the stratagems or the keybinds to call them in, update [codes.json](codes.json) or [keybinds.json](keybinds.json) respectively. Running [genscripts.py](genscripts.py) using any Python interpreter will put a DuckyScript for each stratagem in [scripts/](scripts/). 

### Updating Stratagem Codes
[codes.json](codes.json) controls the stratagem names and codes. Each stratagem entry follows the format: `"NAME":"CODE"`. `NAME` is whatever you want the script for that stratagem to be named. `CODE` is the names of the arrow key presses in sequence, separated by spaces and in all caps, to activate the stratagem. For example, the "Resupply" stratagem is called by pressing the down arrow twice, then the up arrow, then the right arrow, so its entry would be:
```
  "Resupply": "DOWN DOWN UP RIGHT"
```
and the corresponding script would be [scripts/Resupply.txt](scripts/Resupply.txt).

[codes.json](codes.json) was initially generated from the HTML of a Helldivers 2 webguide, cited in References and saved in [readcodes/](readcodes/).

### Customizing Keybinds
[keybinds.json](keybinds.json) translates between arrow directions and your custom keybindings. If you hold `shift` to enter stratagems, and key them in using `wasd` with a delay of 100 milliseconds between button presses, your keybinds file would look like:
```
{
    "CTRL": "SHIFT",
    "UP": "w",
    "LEFT": "a",
    "DOWN": "s",
    "RIGHT": "d",
    "DELAY": 100
}
```

## References
- https://www.shacknews.com/article/138705/all-stratagems-codes-helldivers-2
- https://payloadstudio.hak5.org/community/
- https://docs.hak5.org/hak5-usb-rubber-ducky/ducky-script-basics/keystroke-injection
