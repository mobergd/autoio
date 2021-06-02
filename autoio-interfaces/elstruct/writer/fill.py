"""
   Useful functions used for all the program writers
"""


import automol
import autowrite as aw
from elstruct.par import Reference, Program
from elstruct.option import is_valid as _option_is_valid
from elstruct.option import name as _option_name
from elstruct.pclass import values as _pclass_values
from elstruct.par import Option
from elstruct.par import program_basis_name
from elstruct.par import program_method_name
from elstruct.par import Method


class TemplateKey():
    """ mako template keys """
    # machine
    MEMORY = 'memory'
    MACHINE_OPTIONS = 'machine_options'
    NPROCS = 'nprocs'
    # theoretical method
    REFERENCE = 'reference'
    METHOD = 'method'
    BASIS = 'basis'
    SCF_OPTIONS = 'scf_options'
    SCF_GUESS_OPTIONS = 'scf_guess_options'
    # molecule / state
    MOL_OPTIONS = 'mol_options'
    CHARGE = 'charge'
    MULT = 'mult'
    SPIN = 'spin'
    GEOM = 'geom'
    ZMAT_VALS = 'zmat_vals'
    ZMAT_VAR_VALS = 'zmat_var_vals'
    ZMAT_CONST_VALS = 'zmat_const_vals'
    FROZEN_DIS_STRS = 'frozen_dis_strs'
    FROZEN_ANG_STRS = 'frozen_ang_strs'
    FROZEN_DIH_STRS = 'frozen_dih_strs'
    COORD_SYS = 'coord_sys'
    SADDLE = 'saddle'
    NUMERICAL = 'numerical'
    # job
    COMMENT = 'comment'
    JOB_KEY = 'job_key'
    JOB_OPTIONS = 'job_options'
    GEN_LINES = 'gen_lines'
    GEN_LINES_1 = 'gen_lines_1'
    GEN_LINES_2 = 'gen_lines_2'
    GEN_LINES_3 = 'gen_lines_3'
    # theoretical method
    BASIS = 'basis'
    SCF_METHOD = 'scf_method'
    SCF_OPTIONS = 'scf_options'
    ISMULTIREF = 'ismultiref'
    CASSCF_OPTIONS = 'casscf_options'
    CORR_METHOD = 'corr_method'
    CORR_OPTIONS = 'corr_options'


# Format strings
def geometry_strings(geo, frozen_coordinates, zma_sign='='):
    """ Build the string for the input geometry

        :param geo: cartesian or z-matrix geometry
        :type geo: tuple
        :param frozen_coordinates: only with z-matrix geometries; list of
            coordinate names to freeze
        :type fozen_coordinates: tuple[str]
        :rtype: (str, str)
    """

    if automol.geom.is_valid(geo):
        geo_str = automol.geom.string(geo)
        zmat_vval_str = ''
        zmat_cval_str = ''
    elif automol.zmat.is_valid(geo):
        zma = geo
        symbs = automol.zmat.symbols(zma)
        key_mat = automol.zmat.key_matrix(zma, shift=1)
        name_mat = automol.zmat.name_matrix(zma)
        val_dct = automol.zmat.value_dictionary(
            zma, angstrom=True, degree=True)
        geo_str = aw.zmat.matrix_block(symbs, key_mat, name_mat)

        vval_dct = {key: val for key, val in val_dct.items()
                    if key not in frozen_coordinates}
        cval_dct = {key: val for key, val in val_dct.items()
                    if key in frozen_coordinates}

        zmat_vval_str = aw.zmat.setval_block(
            vval_dct, setval_sign=zma_sign).strip()
        zmat_cval_str = aw.zmat.setval_block(
            cval_dct, setval_sign=zma_sign).strip()
    elif geo in ('GEOMETRY', 'GEOMETRY_HERE'):
        geo_str = geo
        zmat_vval_str = ''
    else:
        raise ValueError("Invalid geometry value:\n{0}".format(geo))

    return geo_str, zmat_vval_str, zmat_cval_str


def _name_mat(zma, frozen_coordinates, job_key):
    """ Build the name matrix for a Z-Matrix data structure:

        used for cfour optimizations

        :param zma: cartesian or z-matrix geometry
        :type zma: tuple
        :param frozen_coordinates: only with z-matrix geometries; list of
            coordinate names to freeze
        :type fozen_coordinates: tuple[str]
        :param job_key: job contained in the inpit file
        :type job_key: str
    """
    if job_key == 'optimization':
        name_mat = [
            [name+'*'
             if name is not None and name not in frozen_coordinates else name
             for name in row]
            for row in automol.zmat.name_matrix(zma)]
    else:
        name_mat = automol.zmat.name_matrix(zma)

    return name_mat


def build_gen_lines(gen_lines, line1=None, line2=None, line3=None):
    """ Set three lines for writing in various blocks of files.
        Function either grabs lines from the dictionary and if nothing
        present, then uses value provided by function
    """

    if gen_lines is not None:
        gen_lines_1 = '\n'.join(gen_lines[1]) if 1 in gen_lines else ''
        gen_lines_2 = '\n'.join(gen_lines[2]) if 2 in gen_lines else ''
        gen_lines_3 = '\n'.join(gen_lines[3]) if 3 in gen_lines else ''
    else:
        gen_lines_1 = ''
        gen_lines_2 = ''
        gen_lines_3 = ''

    if not gen_lines_1:
        gen_lines_1 = line1 if line1 is not None else ''
    if not gen_lines_2:
        gen_lines_2 = line2 if line2 is not None else ''
    if not gen_lines_3:
        gen_lines_3 = line3 if line3 is not None else ''

    return gen_lines_1, gen_lines_2, gen_lines_3


# Handle setting options for various programs
def evaluate_options(options, option_eval_dct):
    """ Build a list of program specific options.

        :param options: requested options.
        :type options: tuple(str)
        :param option_eval_dct: program specific values for an options
        :type option_eval_dct: dict[str: str]
        :type: dict[str: str]
    """

    options = list(options)
    option_names = tuple(sorted(option_eval_dct.keys()))
    for idx, option in enumerate(options):
        if _option_is_valid(option):  # failing for some reason
            name = _option_name(option)
            assert name in option_names
            options[idx] = option_eval_dct[name](option)

    return tuple(options)


def intercept_scf_guess_option(options, option_eval_dct):
    """ Set SCF guess options

        :param options: requested options.
        :type options: tuple(str)
        :param option_eval_dct: program specific values for an options
        :type option_eval_dct: dict[str: str]
        :rtype: (tuple(str), tuple(str))
    """

    guess_options = []
    scf_options = []
    for opt in options:
        if (_option_is_valid(opt) and opt in
                _pclass_values(Option.Scf.Guess)):
            guess_options.append(opt)
        else:
            scf_options.append(opt)
    scf_guess_options = evaluate_options(guess_options, option_eval_dct)
    scf_options = evaluate_options(scf_options, option_eval_dct)

    return scf_guess_options, scf_options


# Set the full description of the theoretical method with
def program_method_names(prog, method, basis, mult, orb_restricted):
    """ Sets all the names of all the components of a theoretical method
        to those specific to the program of interest so that a proper input
        file can be written.

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param method: electronic structure method
        :type method: str
        :param basis: basis set
        :type basis: str
        :param mult: spin multiplicity
        :type mult: int
        :param orb_restricted: parameter designating if restriced refrence used
        :type orb_restricted: bool
        :rtype: (str, str, str)
    """

    # Determine the reference for the given method
    prog_reference = _reference(prog, method, mult, orb_restricted)

    # Determine the method
    if Method.is_casscf(method):
        prog_method = prog_reference
    elif method == Method.HF[0]:
        if prog in (Program.GAUSSIAN09, Program.GAUSSIAN16):
            prog_method = prog_reference
        else:
            prog_method = program_method_name(prog, method)
    else:
        prog_method = program_method_name(prog, method)

    # Set the basis
    prog_basis = program_basis_name(prog, basis)

    return prog_method, prog_reference, prog_basis


def _reference(prog, method, mult, orb_restricted):
    """ Determine the string for what the Hartree-Fock or Kohn-Sham
        reference should be based on the electronic structure method
        and electronic structure program is.

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param method: electronic structure method
        :type method: str
        :param mult: spin multiplicity
        :type mult: int
        :param orb_restricted: parameter designating if restriced refrence used
        :type orb_restricted: bool
        :rtype: str
    """
    # Need a multiref version
    if Method.is_dft(method):
        reference = _dft_reference(prog, orb_restricted)
    elif method == Method.HF[0]:
        reference = _hf_reference(prog, mult, orb_restricted)
    else:
        reference = _corr_reference(prog, mult, orb_restricted)

    return reference


def _dft_reference(prog, orb_restricted):
    """ dft
    """
    if prog in (Program.GAUSSIAN09, Program.GAUSSIAN16):
        reference = ''
    else:
        reference = (Reference.RKS if orb_restricted else
                     Reference.UKS)

    return reference


def _hf_reference(prog, mult, orb_restricted):
    """ hf
    """
    if prog in (Program.GAUSSIAN09, Program.GAUSSIAN16):
        reference = ''
    else:
        if mult == 1:
            reference = Reference.RHF
        else:
            reference = (Reference.ROHF if orb_restricted else
                         Reference.UHF)

    if reference == Reference.ROHF:
        if prog == Program.MOLPRO2015:
            reference = Reference.RHF

    return reference


def _corr_reference(prog, mult, orb_restricted):
    """ correlated method reference
    """
    if mult == 1:
        reference = Reference.RHF
    else:
        reference = (Reference.ROHF if orb_restricted else
                     Reference.UHF)

    if reference == Reference.ROHF:
        if prog == Program.MOLPRO2015:
            reference = Reference.RHF

    return reference
