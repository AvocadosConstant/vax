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

COLOR = {
    'BLACK':    0,
    'RED':      1,
    'GREEN':    2,
    'YELLOW':   3,
    'BLUE':     4,
    'MAGENTA':  5,
    'CYAN':     6,
    'WHITE':    7,
    'DEFAULT':  9
}


def fg(color):
    return str(COLOR[color] + 30)

def bg(color):
    return str(COLOR[color] + 40)

def format_text(text, *args):
    attrs = ';'.join(args)
    return f'{CSI}{attrs}m{text}{RESET}m'
