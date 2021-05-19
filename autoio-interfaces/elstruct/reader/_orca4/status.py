""" status checkers
"""
import autoparse.pattern as app
import autoparse.find as apf
import elstruct.par


def has_normal_exit_message(output_string):
    """ does this output string have a normal exit message?
    """
    pattern = app.escape('****ORCA TERMINATED NORMALLY****')
    return apf.has_match(pattern, output_string, case=False)


def _has_scf_nonconvergence_error_message(output_string):
    """ does this output string have an SCF non-convergence message?
    """
    pattern = 'This wavefunction IS NOT CONVERGED!'
    return apf.has_match(pattern, output_string, case=False)


def _has_cc_nonconvergence_error_message(output_string):
    """ does this output string have a CC non-convergence message?
    """
    pattern = '--- The Coupled-Cluster iterations have NOT converged ---'
    return apf.has_match(pattern, output_string, case=False)


def _has_opt_nonconvergence_error_message(output_string):
    """ does this output string have an optimization non-convergence message?
    """
    pattern = ('The optimization has not yet converged - ' +
               'more geometry cycles are needed')
    return apf.has_match(pattern, output_string, case=False)


ERROR_READER_DCT = {
    elstruct.par.Error.SCF_NOCONV: _has_scf_nonconvergence_error_message,
    elstruct.par.Error.OPT_NOCONV: _has_opt_nonconvergence_error_message,
}


def error_list():
    """ list of errors that be identified from the output file
    """
    return tuple(sorted(ERROR_READER_DCT.keys()))


def has_error_message(error, output_string):
    """ does this output string have an error message?
    """
    assert error in error_list()
    # get the appropriate reader and call it
    error_reader = ERROR_READER_DCT[error]
    return error_reader(output_string)


def check_convergence_messages(error, success, output_string):
    """ check if error messages should trigger job success or failure
    """
    assert error in error_list()
    # assert success in sucess_list()
    _ = success

    job_success = True
    has_error = ERROR_READER_DCT[error](output_string)
    if has_error:
        job_success = False

    return job_success
