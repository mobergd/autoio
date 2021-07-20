""" Parses the DiNT input file
"""

import sys
import ioformat
import automol
import autoparse.pattern as app
import autoparse.find as apf

# Required and Supported keywords for the input
SUPPORTED_KEYS = {
    'run_info': ('POTFLAG', 'nsurf0', 'nsurft',
                 'METHFLAG', 'REPFLAG', 'INTFLAG',
                 'hstep0', 'eps', 'hstep', 'nprint', 'ranseed',
                 'ntraj', 'TFLAG1', 'TFLAG2', 'TFLAG3', 'TFLAG4',
                 'nmol', 'ezero'),
    'ag': ('natom', 'INITx', 'INITp', 'INITj',
           'ezeroi', 'geom', 'temp0im', 'escale0im', 'samptarg',
           'sampjmin', 'sampjmax', 'sampjtemp1', 'sampjtemp2',
           'sampbrot1', 'sampbrot2'),
    'collision': ('TERMFLAG', 'tnstep', 'tgradmag',
                  'ioutput', 'ilist')
}
REQUIRED_KEYS = {
    'run_info': ('POTFLAG', 'nsurf0', 'nsurft',
                 'METHFLAG', 'REPFLAG', 'INTFLAG',
                 'nprint', 'ranseed',
                 'ntraj', 'TFLAG1', 'TFLAG2', 'TFLAG3', 'TFLAG4',
                 'nmol', 'ezero'),
    'ag': ('natom', 'INITx', 'INITp', 'INITj',
           'ezeroi', 'geom'),
    'collision': ('TERMFLAG', 'ioutput', 'ilist')
}

# Defaults for keys that may be missing
#DEFAULT_DCT = {
#    'Units': ''
#}

# Parse the input string
def input_file(input_file):
    """ Parse the input file into defined blocks
    """

    # Parse the sections of the input into keyword-val dictionaries
    run_block = ioformat.ptt.symb_block(input_file, '$', 'run_info')
    ag_block = ioformat.ptt.symb_block(input_file, '$', 'ag')
    coll_block = ioformat.ptt.symb_block(input_file, '$', 'collision')
    exec_block = ioformat.ptt.symb_block(input_file, '$', 'cl_exec')

    run_dct = ioformat.ptt.keyword_dct_from_block(
        run_block[1], formatvals=False)
    ag_dct = ioformat.ptt.keyword_dct_from_block(
        ag_block[1], formatvals=False)
    coll_dct = ioformat.ptt.keyword_dct_from_block(
        coll_block[1], formatvals=False)
    exec_dct = ioformat.ptt.keyword_dct_from_block(
        exec_block[1], formatvals=False)

    # Set defaults (maybe use fancy version later if more defaults can be set)
#    if 'Units' not in run_dct:
#        run_dct['Units'] = DEFAULT_DCT['Units']

    # Check that the dictionaries are built correctly
    _check_dcts(run_dct, ag_dct, coll_dct, exec_dct)

    return run_dct, ag_dct, coll_dct, exec_dct


def opt_geometry(output_str):
    """ Read optimized geometry from DiNT output
    """
    "At the geometry"
    ptt = app.padded(app.NEWLINE).join([
        app.escape('At the geometry'),
        '',
        app.UNSIGNED_INTEGER,
        (app.one_or_more(app.NEWLINE) + app.SPACES),
        app.escape('Calculated rotational constants for this structure:')
    ])

    symbs, xyzs = ar.geom.read(
        output_str,
        start_ptt=ptt)
    geom = automol.geom.from_data(symbs, xyzs, angstrom=True)

    return geom


def rot_consts(output_str):
    """ Read symmetrized rotational constants from DiNT output
    """
    " Symmetrized to   0.65998994499494590       (x2) and    2.7235984942953118       cm-1"
    rot_ptt = (app.SPACES + 'Symmetrized to' + app.SPACES + 
                app.capturing(app.FLOAT) + app.SPACES + '(x2) and' +
                app.SPACES + app.capturing(app.FLOAT) + app.SPACES + 'cm-1'
    )

    rot_cons = apf.all_captures(rot_ptt, output_str)
    if rot_cons is not None:
        rot_cons = tuple(float(val) for val in rot_cons)

    return rot_cons


def energy(output_str):
    """ Read minimum energy from DiNT output
    """
    "Energy conservation"
    " Converged to         =    -0.92274638E-02 eV"
    pattern = (app.SPACES + 'Converged to' + app.SPACES + '=' +
              app.capturing(app.FLOAT) + app.SPACES + 'eV'
    )

    energy = apf.first_capture(pattern, output_str)

    return energy


def alpha(output_str):
    """ Read value of alpha from DiNT output
    """

    pattern = (app.SPACES + 'Converged to' + app.SPACES + '=' +
              app.capturing(app.FLOAT) + app.SPACES + 'eV'
    )

    alpha = apf.first_capture(pattern, output_str)

    return alpha


def _check_dcts(run_dct, ag_dct, coll_dct, exec_dct):
    """ Assess if the dicts are build correctly
    """

    chk_info = zip((run_dct, ag_dct, coll_dct, exec_dct),
                   ('training_data', 'functional_form', 'fortran_execution'))

    for dct, name in chk_info:
        # Assess if a required section was defined in the input
        if dct is None:
            print('Section: {} not defined in input'.format(name))
            sys.exit()
        else:
            # Get the keywords that the user defined in the input
            defined_keys = set(dct.keys())

            # Check if only supported keys defined
            supp_keys = set(SUPPORTED_KEYS[name])
            unsupported_defined_keys = defined_keys - supp_keys
            if unsupported_defined_keys:
                print('Unsupported keywords given in section {}'.format(name))
                for key in unsupported_defined_keys:
                    print(key)
                sys.exit()

            # Check if all required keys defined
            req_keys = set(REQUIRED_KEYS[name])
            undefined_required_keys = req_keys - defined_keys
            if undefined_required_keys:
                print('Required keywords not given in section {}'.format(name))
                for key in undefined_required_keys:
                    print(key)
                sys.exit()

    # Need a secondary check on the exec dct
#    if exec_dct['UseCL'] == 'T':
#        if 'CommandLine' not in exec_dct:
#            print('CommandLine must be given in fortran_execution ',
#                  'if UseCL set to T')
#            sys.exit()
