"""
Executes the automation part of DiNT 
"""

import os
from mako.template import Template


# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')

########## Optimization ##########

def dint_opt(potflag, nsurf0, nsurft, methflag, repflag, 
             intflag, hstep0, eps, nprint, ranseed, ntraj,
             tflag1, tflag2, tflag3, tflag4, nmol, ezero,
             natom, initx, initp, initj, ezeroi, geom,
             termflag, tnstep?, tgradmag, ioutput, ilist):
    """ writes the DiNT input file for an optimziation job """

    # Set the dictionary for the DiNT opt input file
    inp_keys = {
        'potflag': potflag,
        'nsurf0': nsurf0,
        'nsurft': nsurft,
        'methflag': methflag,
        'repflag': repflag,
        'intflag': intflag,
        'hstep0': hstep0,
        'eps': eps,
        'nprint': nprint,
        'ranseed': ranseed,
        'ntraj': ntraj,
        'tflag1': tflag1,
        'tflag2': tflag2,
        'tflag3': tflag3,
        'tflag4': tflag4,
        'nmol': nmol,
        'ezero': ezero,
        'natom': natom,
        'initx': initx,
        'initp': initp,
        'initj': initj,
        'ezeroi': ezeroi,
        'geom': geom,
        'termflag': termflag,
        'tnstep'?: tnstep,
        'tgradmag': tgradmag,
        'ioutput': ioutput,
        'ilist': ilist
    }

    return build_mako_opt(
        template_file_name='dint_opt.mako'
        template_src_path=TEMPLATE_PATH,
        template_keys=inp_keys)


########## Sampling ##########

def dint_samp(potflag, nsurf0, nsurft, methflag, repflag, 
             intflag, hstep0, eps, nprint, ranseed, ntraj,
             tflag1, tflag2, tflag3, tflag4, nmol, ezero,
             natom, initx, initp, initj, ezeroi, geom,
             termflag, tnstep?, tgradmag, ioutput, ilist):
    """ writes the DiNT input file for an optimziation job """

    # Set the dictionary for the DiNT opt input file
    inp_keys = {
        'potflag': potflag,
        'nsurf0': nsurf0,
        'nsurft': nsurft,
        'methflag': methflag,
        'repflag': repflag,
        'intflag': intflag,
        'hstep0': hstep0,
        'eps': eps,
        'nprint': nprint,
        'ranseed': ranseed,
        'ntraj': ntraj,
        'tflag1': tflag1,
        'tflag2': tflag2,
        'tflag3': tflag3,
        'tflag4': tflag4,
        'nmol': nmol,
        'ezero': ezero,
        'natom': natom,
        'initx': initx,
        'initp': initp,
        'initj': initj,
        'ezeroi': ezeroi,
        'geom': geom,
        'termflag': termflag,
        'tnstep'?: tnstep,
        'tgradmag': tgradmag,
        'ioutput': ioutput,
        'ilist': ilist
    }

    return build_mako_opt(
        template_file_name='dint_opt.mako'
        template_src_path=TEMPLATE_PATH,
        template_keys=inp_keys)

########## Trajectories ##########

def dint_traj(potflag, nsurf0, nsurft, methflag, repflag, 
             intflag, hstep0, eps, nprint, ranseed, ntraj,
             tflag1, tflag2, tflag3, tflag4, nmol, ezero,
             natom, initx, initp, initj, ezeroi, geom,
             termflag, tnstep?, tgradmag, ioutput, ilist):
    """ writes the DiNT input file for an optimziation job """

    # Set the dictionary for the DiNT opt input file
    inp_keys = {
        'potflag': potflag,
        'nsurf0': nsurf0,
        'nsurft': nsurft,
        'methflag': methflag,
        'repflag': repflag,
        'intflag': intflag,
        'hstep0': hstep0,
        'eps': eps,
        'nprint': nprint,
        'ranseed': ranseed,
        'ntraj': ntraj,
        'tflag1': tflag1,
        'tflag2': tflag2,
        'tflag3': tflag3,
        'tflag4': tflag4,
        'nmol': nmol,
        'ezero': ezero,
        'natom': natom,
        'initx': initx,
        'initp': initp,
        'initj': initj,
        'ezeroi': ezeroi,
        'geom': geom,
        'termflag': termflag,
        'tnstep'?: tnstep,
        'tgradmag': tgradmag,
        'ioutput': ioutput,
        'ilist': ilist
    }

    return build_mako_opt(
        template_file_name='dint_opt.mako'
        template_src_path=TEMPLATE_PATH,
        template_keys=inp_keys)

### WIP
def submission_script(drive_path, run_path, njobs):
    """ launches the job """

    # Write the bottom of the string
    job_exe_lines = '# Run several dint.x instances\n'
    job_exe_lines += 'cd {0}/run1\n'.format(run_path)
    job_exe_lines += 'time $DINTEXE < input.dat > output.dat &\n'
    for i in range(njobs-1):
        job_exe_lines += 'cd ../run{0}\n'.format(str(i+2))
        job_exe_lines += 'time $DINTEXE < input.dat > output.dat &\n'
    job_exe_lines += 'wait\n'

    # Set the dictionary for the DiNT input file
    fill_vals = {
        "job_exe_lines": job_exe_lines,
    }

    # Set template name and path for the DiNT input file
    template_file_name = 'submit.mako'
    template_file_path = os.path.join(drive_path, template_file_name)

    # Build the 1dmin input string
    sub_str = Template(filename=template_file_path).render(**fill_vals)

    return sub_str
