"""
ANSI Escape Codes

See https://en.wikipedia.org/wiki/ANSI_escape_code
"""

# Control Sequence Introducer
CSI =           '\x1b['
RESET =         f'{CSI}0' 

BOLD =          '1'
UNDERLINE =     '4'
REVERSE =       '7'

FG_BLACK =      '30'
FG_RED =        '31'
FG_GREEN =      '32'
FG_YELLOW =     '33'
FG_BLUE =       '34'
FG_MAGENTA =    '35'
FG_CYAN =       '36'
FG_WHITE =      '37'
FG_DEFAULT =    '39'

BG_BLACK =      '40'
BG_RED =        '41'
BG_GREEN =      '42'
BG_YELLOW =     '43'
BG_BLUE =       '44'
BG_MAGENTA =    '45'
BG_CYAN =       '46'
BG_WHITE =      '47'
BG_GRAY =       '100'
BG_DEFAULT =    '49'


def format(text, *args):
    attrs = ';'.join(args)
    return f'{CSI}{attrs}m{text}{RESET}m'
