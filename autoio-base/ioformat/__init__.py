""" Library of functions for writing and formatting strings
    that are used by all of the interface modules
"""

from ioformat._format import build_mako_str
from ioformat._format import indent
from ioformat._format import add_line
from ioformat._format import change_line
from ioformat._format import addchar
from ioformat._format import headlined_sections
from ioformat._format import remove_whitespace_from_string
from ioformat._format import remove_trail_whitespace
from ioformat._format import remove_comment_lines
from ioformat import pathtools
from ioformat import phycon
from ioformat import ptt


__all__ = [
    'build_mako_str',
    'indent',
    'add_line',
    'change_line',
    'addchar',
    'headlined_sections',
    'remove_whitespace_from_string',
    'remove_trail_whitespace',
    'remove_comment_lines',
    'addchar',
    'pathtools',
    'phycon',
    'ptt'
]
