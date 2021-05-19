""" Tests the writing of the energy transfer section
"""

import os
from ioformat import read_text_file
import mess_io.writer


# Atom/Molecule Data
PATH = os.path.dirname(os.path.realpath(__file__))
CORE_STR = """  Geometry[angstrom]        8
    C         -0.75583       0.00710      -0.01604
    C          0.75582      -0.00710       0.01604
    H         -1.16275      -0.10176       0.99371
    H         -1.12255       0.94866      -0.43557
    H         -1.13499      -0.81475      -0.63070
    H          1.13499       0.81475       0.63070
    H          1.16275       0.10176      -0.99371
    H          1.12255      -0.94866       0.43557
  Core RigidRotor
    SymmetryFactor          3.0
  End"""
FREQS = (10.0, 100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0,
         1000.0, 1100.0, 1200.0, 1300.0, 1400.0, 1500.0, 1600.0, 1700.0)
FREQ_SCALE_FACTOR = 1.833
INF_INTENS = (1.0, 11.0, 22.0, 33.0, 44.0, 55.0, 66.0, 77.0, 88.0, 99.0,
              110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0, 180.0)
MASS = 16.0
ELEC_LEVELS1 = ((1, 0.00), (3, 150.0), (9, 450.0))
ELEC_LEVELS2 = ((1, 0.00),)
HR_STR = """Rotor  Hindered
  Group                11  10  9   8   7   6
  Axis                 3   2   1
  Symmetry             1
  Potential[kcal/mol]  12
    0.00    2.91    9.06    12.63   9.97    3.51
    0.03    3.49    9.96    12.63   9.08    2.93
End"""
XMAT = ((10000, 2000, 4000),
        (2000, 3000, 5000),
        (4000, 5000, 6000))
ROVIB_COUPS = (100, 200, 300)
ROT_DISTS = (('aaaa', 1000), ('bbaa', 2000), ('bbbb', 3000))


def test__atom_writer():
    """ Writes a string containing all info for an atom in MESS style
    """

    atom_str = mess_io.writer.atom(MASS, ELEC_LEVELS1)
    assert atom_str == read_text_file(['data', 'inp'], 'atom_data.inp', PATH)


def test__molecule_writer():
    """ Writes a string containing all info for a molecule in MESS style
    """

    mol1_str = mess_io.writer.molecule(
        CORE_STR, ELEC_LEVELS2)
    assert mol1_str == read_text_file(['data', 'inp'], 'mol1_data.inp', PATH)

    mol2_str = mess_io.writer.molecule(
        CORE_STR, ELEC_LEVELS2,
        freqs=FREQS,
        freq_scale_factor=FREQ_SCALE_FACTOR,
        use_harmfreqs_key=True)
    assert mol2_str == read_text_file(['data', 'inp'], 'mol2_data.inp', PATH)

    mol3_str = mess_io.writer.molecule(
        CORE_STR, ELEC_LEVELS2,
        freqs=FREQS, hind_rot=HR_STR,
        xmat=XMAT,
        rovib_coups=ROVIB_COUPS,
        rot_dists=ROT_DISTS,
        inf_intens=INF_INTENS)
    assert mol3_str == read_text_file(['data', 'inp'], 'mol3_data.inp', PATH)


if __name__ == '__main__':
    test__atom_writer()
    test__molecule_writer()
