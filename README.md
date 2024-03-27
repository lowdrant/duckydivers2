# duckydivers
Rubber ducky scripts for calling in stratagems in HellDivers 2.

## Updating Stratagem Codes
Stratagem codes are stored as entries in [codes.json](codes.json). Entries follow the format `"NAME":"CODE"`. `NAME` is any string. `CODE` is the names of the arrow key presses in sequence, separated by spaces and in all caps, to activate the stratagem. For example, the "Resupply" stratagem is called by pressing the down arrow twice, then the up arrow, then the right arrow, so its entry would be:
```
  "Resupply": "DOWN DOWN UP RIGHT"
```

[codes.json](codes.json) was initially generated from the HTML of a Helldivers 2 webguide, cited below and saved in [readcodes/](readcodes/).

## Customizing Keybinds
[keybinds.json](keybinds.json) translates between the default Helldivers 2 keybindings and custom keybindings. For example, if you hold `shift` to enter stratagems, and key them in using `wasd` with a delay of 100 milliseconds between button presses, your keybinds file would look like:
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
