""" Parses the DiNT input file
"""

import sys
import ioformat
import autoread.geom as apg

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
def input_file(inp_str):
    """ Parse the input string
    """

    # Parse the sections of the input into keyword-val dictionaries
    run_block = ioformat.ptt.symb_block(inp_str, '$', 'run_info')
    ag_block = ioformat.ptt.symb_block(inp_str, '$', 'ag')
    coll_block = ioformat.ptt.symb_block(inp_str, '$', 'collision')

    run_dct = ioformat.ptt.keyword_dct_from_block(
        run_block[1], formatvals=False)
    ag_dct = ioformat.ptt.keyword_dct_from_block(
        ag_block[1], formatvals=False)
    coll_dct = ioformat.ptt.keyword_dct_from_block(
        coll_block[1], formatvals=False)

    # Set defaults (maybe use fancy version later if more defaults can be set)
#    if 'Units' not in run_dct:
#        run_dct['Units'] = DEFAULT_DCT['Units']

    # Check that the dictionaries are built correctly
    _check_dcts(run_dct, ag_dct, coll_dct)

    return run_dct, ag_dct, coll_dct

def _check_dcts(run_dct, ag_dct, coll_dct):
    """ Assess if the dicts are build correctly
    """

    chk_info = zip((run_dct, ag_dct, coll_dct),
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
