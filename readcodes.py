#!/usr/bin/env python3
"""CLI to webscrape stragagem entry codes and store in JSON for duckyscript"""
if __name__ != '__main__':
    raise RuntimeError('Is a CLI')
from argparse import ArgumentParser
from json import dump
from pathlib import Path
from re import compile as re_compile
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
DEFAULT_FNJSON = ROOT / 'codes.json'
DEFAULT_FNKEYS = ROOT / 'keybinds.json'
SCRIPTDIR = ROOT / 'scripts'

# =============================================================================
# INTERFACE CLASSES
# =============================================================================


class AbstractCodesFromWeb:
    """Abstract superclass for webscraping Helldivers 2 (HD2) stratagem codes
        and storing them in a JSON file.

        OVERVIEW:
            The first step in creating HD2 stratagem duckyscripts is determing
            the stratagem names and entry codes. This abstract superclass
            provides an interface to (1) download HTML from a webpage with the
            stratagem codes in plaintext, (2) parse the HTML to pair the
            stratagems with their codes, and (3) save the pairs in a JSON.
            Another program then takes the JSON and turns it into Duckscripts.

        ABSTRACT:
            URL -- str -- wbbpage to download codes from 
            parse -- method -- parses `self.lines` into `self.codes`
            KEYUP -- str -- string in html corresponding to key-up in HD2
            KEYDOWN -- str -- string in html corresponding to key-down in HD2
            KEYLEFT -- str -- string in html corresponding to key-left in HD2
            KEYRIGHT -- str -- string in html corresponding to key-right in HD2


        ATTRIBUTES:
            resp -- urlopen output
            block -- resp html converted from bytes to str
            lines -- list of plaintext lines in resp html
            codes -- dict mapping stratagem name to entry code

        CONCRETE USAGE:
            >>> src = ClassName()
            >>> src.download()
            >>> src.parse()
            >>> src.save(filename)
    """
    URL = None
    KEYLEFT = None
    KEYRIGHT = None
    KEYUP = None
    KEYDOWN = None

    def __init__(self):
        self.resp = None
        self.block = None
        self.lines = None
        self.codes = {}
        self.keydict = {self.KEYDOWN: 'DOWN',
                        self.KEYUP: 'UP',
                        self.KEYLEFT: 'LEFT',
                        self.KEYRIGHT: 'RIGHT'}

    def _raise_abstract_err(self):
        raise NotImplementedError('Abstract method')

    def download(self):
        """Download HTML from self.URL and convert it into plaintext."""
        self.resp = urlopen(self.URL)  # attr for debugging
        # determine text encoding
        ct = self.resp.getheader('Content-Type')
        if ct is None:
            raise RuntimeError(f'Failed to read content type from {self.URL}')
        for v in ct.split(';'):
            i = v.lower().find('charset')
            if i != -1:
                encoding = v.split('=')[1]
                break
        valid_enc = any([v in encoding.lower() for v in ['utf-8']])
        assert valid_enc, f'Bad encoding: {encoding}'
        # convert to plain text
        self.block = self.resp.read().decode(encoding)  # attr for debugging
        self.lines = self.block.splitlines()

    def parse(self):
        self._raise_abstract_err()

    def save(self, fn):
        with open(fn, 'w') as f:
            ret = dump(self.codes, f, indent=1)
        return ret

    def _addcode(self, name, codeseq):
        """Add `name` hash to self.codes with codeseq translated by keydict"""
        self.codes.update({name: ' '.join(self.keydict[c] for c in codeseq)})

    def haskey(self, line):
        """Check if line of html has entry key"""
        return any([k in line for k in self.keydict])


class CodesFromShackNews(AbstractCodesFromWeb):
    URL = "https://www.shacknews.com/article/138705/all-stratagems-codes-helldivers-2"
    KEYLEFT = '&larr'
    KEYRIGHT = '&rarr'
    KEYUP = '&uarr'
    KEYDOWN = '&darr'

    def parse(self):
        # Identify Stratagems
        # - Table format goes "Name"\n"Code". Codes are easier to find, so
        # - find the codes and then get the name from the previous line.
        for i, line in enumerate(self.lines):
            if self.haskey(line):
                codeseq = self._striphtml(line).split(';')[:-1]
                # only consider stratagem code lines
                if all([v in self.keydict for v in codeseq]):
                    self._addcode(self._striphtml(self.lines[i - 1]), codeseq)

    @staticmethod
    def _striphtml(txt):
        """Stratagem info stored in tables. Return the relevant raw text."""
        txt = txt.strip()
        i1 = txt[:-1].rfind(';">') + 3  # start of entry
        i2 = txt.rfind('</td>')  # end of entry
        return txt[i1:i2]


class CodesFromGG(AbstractCodesFromWeb):
    """Download HD2 codes from wiki.gg"""
    # robots.txt seems to allow webscraping, but I get 403 trying to get it
    URL = Request('https://helldivers.wiki.gg/wiki/Stratagems',
                  headers={'User-Agent': 'Mozilla/5.0'})
    KEYLEFT = 'Left Arrow.png'
    KEYRIGHT = 'Right Arrow.png'
    KEYUP = 'Up Arrow.png'
    KEYDOWN = 'Down Arrow.png'

    def parse(self):
        i = 0
        while i < len(self.lines):
            if self.haskey(self.lines[i]):
                name = self.lines[i - 3].split('>')[-2][:-3]
                arrow_idxs = [i]
                # search for end of stratagem code
                # - same-stratagem keys have spacing of 2
                while self.haskey(self.lines[i + 2]):
                    i += 2
                    arrow_idxs.append(i)
                codeseq = [self.lines[j].split('"')[1] for j in arrow_idxs]
                self._addcode(name, codeseq)
                i = arrow_idxs[-1]  # +1 added at end of loop
            i += 1


class CodesFromFandom(AbstractCodesFromWeb):
    """Download codes from https://helldivers.fandom.com."""
    URL = 'https://helldivers.fandom.com/wiki/Stratagem_Codes_(Helldivers_2)'
    KEYLEFT = '"Left Arrow"'
    KEYRIGHT = '"Right Arrow"'
    KEYUP = '"Up Arrow"'
    KEYDOWN = '"Down Arrow"'

    def parse(self):
        expr = re_compile('"[A-Z][a-z]+ Arrow"')
        for i, line in enumerate(self.lines):
            if self.haskey(line):
                name = self.lines[i - 2].split('>')[-2][:-3]
                codeseq = expr.findall(line)
                self._addcode(name, codeseq)

# =============================================================================
# DUCKYSCRIPT
# =============================================================================


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


def writecodes(codes, keybinds):
    """Write codes to duckyscripts using keybinds"""
    for n, c in codes.items():
        c = c.upper()  # enforce uppercase
        script = genducky(n, c, keybinds)
        with open(SCRIPTDIR / (n + '.txt'), 'w') as f:
            f.write(script)

# =============================================================================
# CLI
# =============================================================================


def cli():
    parser = ArgumentParser('CLI to webscrape stratagem entry codes and turn them into duckscripts
                            )
    subparsers = parser.add_subparsers(help='subcmd help', dest='cmd')

    # Download CLI
    parser_download = subparsers.add_parser('download', help='download help')
    parser_download.add_argument(
        '--fn', type=str, default=DEFAULT_FNJSON, help='where to store downloaded codes')
    parser_download.add_argument(
        '--src', choices=['fandom', 'gg', 'shacknews'], help='asdf')

    # Write CLI
    parser_write = subparsers.add_parser('write', help='write help')
    parser_write.add_argument(
        '--fnjson', type=str, default=DEFAULT_FNJSON, help='where to store downloaded codes')
    parser_write.add_argument('--fnkeys', type=str,
                              default=DEFAULT_FNKEYS, help='keybinds cfg')

    # All CLI
    parser_all = subparsers.add_parser('all')
    parser_all.add_argument('--fnkey', type=str,
                            default=DEFAULT_FNKEYS, help='keybinds cfg')
    parser = setup_cli()
    args = parser.parse_args()


def main():
    args = cl()
    if cmd in ('download', 'all'):
        if args.src == 'fandom':
            src = CodesFromFandom()
        elif args.src == 'gg':
            src = CodesFromGG()
        elif args.src == 'shacknews':
            src = CodesFromShackNews()
        src.download()
        src.parse()
        src.save(args.fn)
    if cmd == 'write':
        writecodes(codes, keybinds)


main()
