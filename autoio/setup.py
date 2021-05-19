""" Install Interfaces to MESS, CHEMKIN, VaReCoF, ProjRot, and ThermP
"""

from distutils.core import setup

setup(
    name="autoio",
    version="0.6.2",
    packages=['mess_io',
              'mess_io.writer',
              'mess_io.reader',
              'projrot_io',
              'polyrate_io',
              'varecof_io',
              'varecof_io.writer',
              'varecof_io.reader',
              'chemkin_io',
              'chemkin_io.writer',
              'chemkin_io.parser',
              'onedmin_io',
              'pac99_io',
              'intder_io',
              'ioformat',
              'thermp_io',
              'dint_io',
              'autoread',
              'autoread',
              'autoread._zmat',
              'autowrite'],
    package_dir={
        'mess_io': 'mess_io',
        'projrot_io': 'projrot_io',
        'varecof_io': 'varecof_io',
        'polyrate_io': 'polyrate_io',
        'chemkin_io': 'chemkin_io',
        'onedmin_io': 'onedmin_io',
        'pac99_io': 'pac99_io',
        'intder_io': 'intder_io',
        'ioformat': 'ioformat',
        'thermp_io': 'thermp_io',
        'dint_io': 'dint_io',
        'autoread': 'autoread',
        'autowrite': 'autowrite'},
    package_data={
        'mess_io': ['writer/templates/sections/*.mako',
                    'writer/templates/sections/energy_transfer/*.mako',
                    'writer/templates/sections/monte_carlo/*.mako',
                    'writer/templates/sections/reaction_channel/*.mako',
                    'writer/templates/species/*.mako',
                    'writer/templates/species/info/*.mako',
                    'tests/data/*.txt'],
        'projrot_io': ['templates/*.mako',
                       'tests/data/*.txt'],
        'polyrate_io': ['tests/templates/*.mako',
                        'templates/*.mako'],
        'onedmin_io': ['tests/templates/*.mako',
                       'templates/*.mako'],
        'varecof_io': ['writer/templates/*.mako',
                       'tests/data/*.txt'],
        'thermp_io': ['templates/*.mako'],
        'dint_io': ['tests/opt/*dat',
                    'tests/samp/*dat',
                    'tests/traj/*dat',
                    'templates/*.mako'],
        'chemkin_io': ['tests/data/*.txt', 'tests/data/*.csv']}
)
