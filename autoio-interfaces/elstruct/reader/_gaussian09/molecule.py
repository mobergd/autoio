""" molecular geometry and structure readers
"""

import numbers
from phydat import ptab
import autoread as ar
import autoparse.pattern as app
import autoparse.find as apf
import automol


def opt_geometry(output_str):
    """ Reads the optimized molecular geometry (in Cartesian coordinates) from
        the output file string. Returns the geometry in Bohr.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: automol molecular geometry data structure
    """

    nums, xyzs = ar.geom.read(
        output_str,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('Standard orientation:'),
            app.LINE, app.LINE, app.LINE, app.LINE, '']),
        symb_ptt=app.UNSIGNED_INTEGER,
        line_start_ptt=app.UNSIGNED_INTEGER,
        line_sep_ptt=app.UNSIGNED_INTEGER,)

    if all(x is None for x in (nums, xyzs)):
        nums, xyzs = ar.geom.read(
            output_str,
            start_ptt=app.padded(app.NEWLINE).join([
                app.escape('Z-Matrix orientation:'),
                app.LINE, app.LINE, app.LINE, app.LINE, '']),
            symb_ptt=app.UNSIGNED_INTEGER,
            line_start_ptt=app.UNSIGNED_INTEGER,
            line_sep_ptt=app.UNSIGNED_INTEGER,)

    if all(x is not None for x in (nums, xyzs)):
        symbs = tuple(map(ptab.to_symbol, nums))
        geo = automol.geom.from_data(symbs, xyzs, angstrom=True)
    else:
        geo = None

    return geo


def opt_zmatrix(output_str):
    """ Reads the optimized Z-Matrix from the output file string.
        Returns the Z-Matrix in Bohr and Radians.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: automol molecular geometry data structure
    """

    if 'Optimized Parameters' in output_str:

        # Reads the matrix from the beginning of the output
        symbs, key_mat, name_mat = ar.vmat.read(
            output_str,
            start_ptt=app.padded(app.NEWLINE).join([
                app.escape('Symbolic Z-matrix:'), app.LINE, '']),
            symb_ptt=(
                ar.par.Pattern.ATOM_SYMBOL +
                app.not_followed_by(app.SPACES + app.FLOAT) +
                app.maybe(app.UNSIGNED_INTEGER)),
            key_ptt=app.one_of_these(
                [app.UNSIGNED_INTEGER, app.VARIABLE_NAME]),
            line_end_ptt=app.maybe(app.UNSIGNED_INTEGER),
            last=False)

        # Reads the values from the end of the output
        if all(x is not None for x in (symbs, key_mat, name_mat)):
            grad_val = app.one_of_these([app.FLOAT, 'nan', '-nan'])
            if len(symbs) == 1:
                # val_dct = {}
                val_mat = ((None, None, None),)
            else:
                val_dct = ar.setval.read(
                    output_str,
                    start_ptt=app.padded(app.NEWLINE).join([
                        app.padded('Optimized Parameters', app.NONNEWLINE),
                        app.LINE, app.LINE, app.LINE, app.LINE, '']),
                    entry_sep_ptt='',
                    entry_start_ptt=app.escape('!'),
                    sep_ptt=app.maybe(app.LINESPACES).join([
                        app.escape('-DE/DX ='), grad_val, app.escape('!'),
                        app.NEWLINE]),
                    last=True)
                val_mat = ar.setval.convert_dct_to_matrix(val_dct, name_mat)

            # Check for the pattern
            err_ptt = app.LINESPACES.join([
                app.escape('-DE/DX ='), app.one_of_these(['nan', '-nan'])])
            if 'Optimized Parameters' in output_str:
                test_str = output_str.split('Optimized Parameters')[1]
                if apf.has_match(err_ptt, test_str):
                    print('Warning: Bad gradient value (nan)',
                          'in "Optimized Parameters" list.')
            # For case when variable names are used instead of integer keys:
            # (otherwise, does nothing)
            key_dct = dict(map(reversed, enumerate(symbs)))
            key_dct[None] = 0
            key_mat = [
                [key_dct[val]+1 if not isinstance(val, numbers.Real) else val
                 for val in row] for row in key_mat]
            symb_ptt = (app.STRING_START +
                        app.capturing(ar.par.Pattern.ATOM_SYMBOL))
            symbs = [apf.first_capture(symb_ptt, symb) for symb in symbs]

            # Call the automol constructor
            zma = automol.zmat.from_data(
                symbs, key_mat, val_mat, name_mat,
                one_indexed=True, angstrom=True, degree=True)
        else:
            zma = None
    else:
        zma = None

    return zma


def inp_zmatrix(inp_str):
    """ Reads the input z-matrix from the input file string
        Returns the Z-Matrix in Bohr and Radians.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: automol molecular geometry data structure
    """

    # Reads the matrix from the beginning of the input
    symbs, key_mat, name_mat = ar.vmat.read(
        inp_str,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('comment:'), app.LINE, app.LINE, '']),
        symb_ptt=(ar.par.Pattern.ATOM_SYMBOL +
                  app.not_followed_by(app.SPACES + app.FLOAT) +
                  app.maybe(app.UNSIGNED_INTEGER)),
        key_ptt=app.one_of_these([app.UNSIGNED_INTEGER, app.VARIABLE_NAME]),
        line_end_ptt=app.maybe(app.UNSIGNED_INTEGER),
        last=False)

    # Reads the values from the input
    if all(x is not None for x in (symbs, key_mat, name_mat)):
        if len(symbs) == 1:
            # val_dct = {}
            val_mat = ((None, None, None),)
        else:
            val_dct = ar.setval.read(
                inp_str,
                start_ptt=app.padded(app.NEWLINE).join([
                    app.padded('Variables:', app.NONNEWLINE), '']),
                entry_sep_ptt='',
                entry_start_ptt='',
                sep_ptt=app.maybe(app.LINESPACES).join([
                    app.NEWLINE]),
                last=True)
            val_mat = ar.setval.convert_dct_to_matrix(val_dct, name_mat)

        # Check for the pattern
        # For the case when variable names are used instead of integer keys:
        # (otherwise, does nothing)
        key_dct = dict(map(reversed, enumerate(symbs)))
        key_dct[None] = 0
        key_mat = [
            [key_dct[val]+1 if not isinstance(val, numbers.Real) else val
             for val in row] for row in key_mat]
        symb_ptt = app.STRING_START + app.capturing(ar.par.Pattern.ATOM_SYMBOL)
        symbs = [apf.first_capture(symb_ptt, symb) for symb in symbs]

        # Call the automol constructor
        zma = automol.zmat.from_data(
            symbs, key_mat, val_mat, name_mat,
            one_indexed=True, angstrom=True, degree=True)
    else:
        zma = None

    return zma
