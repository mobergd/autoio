""" Read DiNT input and output files
"""

import os
import numpy
from ioformat import read_text_file
import onedmin_io.reader


PATH = os.path.dirname(os.path.realpath(__file__))
INP_STR = read_text_file(['data'], 'input-opt.dat', PATH)
ONEDMIN_OUT_STR = read_text_file(['data'], 'onedmin.out', PATH)


def test__input_file():
    """ test dint_io.parser.input_file
    """

    ref_potflag  = 2
    ref_nsurf0   = 1
    ref_nsurft   = 1
    ref_METHFLAG = 0
    ref_REPFLAG  = 0
    ref_INTFLAG  = 0
    ref_hstep0   = 1.
    ref_eps      = 1.d-6
    ref_nprint   = 1
    ref_RANSEED  = 80538343
    ref_ntraj    = 1
    ref_TFLAG1   = 1
    ref_TFLAG2   = 0
    ref_TFLAG3   = 0
    ref_TFLAG4   = 0
    ref_nmol     = 1
    ref_ezero    = 0.
    ref_natom    = 6
    ref_INITx    = 0
    ref_INITp    = 1
    ref_INITj    = 0
    ref_ezeroi   = 0.
    ref_geom     = {
C                -0.02812963           0.72386574          -0.00000000
O                -0.02914129          -0.68613354           0.00000000
O                 0.88103041          -0.99139908           0.00000000
H                -1.05549799           1.08802723          -0.00000000
H                 0.48594566           1.08692129           0.88995314
H                 0.48594566           1.08692129          -0.88995314
}
    ref_TERMFLAG = 2
    ref_tnstep   = 10000
    ref_tgradmag = 0.001
    ref_ioutput  = 1
    ref_ilist    = 77


    ref_sigmas = (6.587188430859643, 6.908800920151311, 6.609902938887646)
    ref_epsilons = (17.88616, 15.23453, 17.731)

    sigmas, epsilons = onedmin_io.reader.lennard_jones(LJ_OUT_STR)

    assert numpy.allclose(ref_sigmas, sigmas)
    assert numpy.allclose(ref_epsilons, epsilons)


def test__program_version():
    """ test onedmin_io.reader.program_version
    """

    ref_prog = '1.0'

    prog = onedmin_io.reader.program_version(ONEDMIN_OUT_STR)

    assert prog == ref_prog
