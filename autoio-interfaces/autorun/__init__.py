"""
  Centralized autorun functions
"""

# Useful Running Functions
from autorun._script import SCRIPT_DCT
from autorun._run import from_input_string
from autorun._run import run_script
from autorun._run import write_input
from autorun._run import read_output

# Single Program Runners
from autorun import mess
from autorun import onedmin
from autorun import pac99
from autorun import polyrate
from autorun import projrot
from autorun import thermp
from autorun import varecof

# MultiProgram Runners
from autorun._multiprog import projected_frequencies
from autorun._multiprog import thermo


__all__ = [
    # Single Program Runners
    'SCRIPT_DCT',
    'run_script',
    'from_input_string',
    'write_input',
    'read_output',
    'mess',
    'onedmin',
    'pac99',
    'polyrate',
    'projrot',
    'thermp',
    'varecof',
    # MultiProgram Runners
    'projected_frequencies',
    'thermo'
]
