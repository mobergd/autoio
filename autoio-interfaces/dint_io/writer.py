"""
Executes the automation part of DiNT 
"""

import os
from ioformat import build_mako_str
#from mako.template import Template


# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')

########## Optimization ##########

def opt_input(potflag, nsurf0, nsurft, methflag, repflag, 
              intflag, hstep0, eps, nprint, ranseed, ntraj,
              tflag1, tflag2, tflag3, tflag4, nmol, ezero,
              natom, initx, initp, initj, ezeroi, geom,
              termflag, tnstep, tgradmag, ioutput, ilist):
    """ writes the DiNT input file for an optimziation job """

    # Set the dictionary for the DiNT opt input file
    inp_keys = {
        # Run info dictionary
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
        # AG info dictionary
        'natom': natom,
        'initx': initx,
        'initp': initp,
        'initj': initj,
        'ezeroi': ezeroi,
        'geom': geom,
        # Collision dictionary
        'termflag': termflag,
        'tnstep': tnstep,
        'tgradmag': tgradmag,
        'ioutput': ioutput,
        'ilist': ilist
#        'UseCL': usecl,
#        'CommandLine': commandline
    }

    return build_mako_str(
        template_file_name='dint_opt.mako',
        template_src_path=TEMPLATE_PATH,
        template_keys=inp_keys)


########## Sampling ##########

def samp_input(potflag, nsurf0, nsurft, methflag, repflag, 
               intflag, hstep, nprint, ranseed, ntraj,
               tflag1, tflag2, tflag3, tflag4, nmol, ezero,
               natom, initx, initp, initj, ezeroi, geom,
               temp0im, escale0im, samptarg, sampjmin, sampjmax, 
               sampjtemp1, sampjtemp2, sampjbrot1, sampjbrot2, 
               termflag, tnstep, tgradmag, ioutput, ilist):
    """ writes the DiNT input file for an optimziation job """

    # Set the dictionary for the DiNT opt input file
    inp_keys = {
        # Run info dictionary
        'potflag': potflag,
        'nsurf0': nsurf0,
        'nsurft': nsurft,
        'methflag': methflag,
        'repflag': repflag,
        'intflag': intflag,
        'hstep': hstep,
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
        'temp0im': temp0im,
        'escale0im': escale0im,
        'samptarg': samptarg,
        'sampjmin': sampjmin,
        'sampjmax': sampjmax,
        'sampjtemp1': sampjtemp1,
        'sampjtemp2': sampjtemp2,
        'sampjbrot1': sampjbrot1,
        'sampjbrot2': sampjbrot2,
        'termflag': termflag,
        'tnstep': tnstep,
        'ioutput': ioutput,
        'ilist': ilist
    }

    return build_mako_str(
        template_file_name='dint_samp.mako',
        template_src_path=TEMPLATE_PATH,
        template_keys=inp_keys)

########## Trajectories ##########

def traj_input(potflag, nsurf0, nsurft, methflag, repflag, 
               intflag, hstep0, eps, nprint, ranseed, ntraj,
               tflag1, tflag2, tflag3, tflag4, nmol, ezero,
               natom, initx, initp, initj, ezeroi, lbinsamp, 
               sampfilexx, sampfilepp, lems, geom, temp0im, escale0im, 
               samptarg, letot, sampjmin, sampjmax, sampjtemp1, sampjtemp2,
               sampjbrot1, sampjbrot2, ejsc1, ejsc2, ejsc3, ejsc4, 
               bath, iorient, ldofrag, termflag, tnstep, tgradmag, 
               ioutput, ilist):
    """ writes the DiNT input file for an optimziation job """

    # Set the dictionary for the DiNT opt input file
    inp_keys = {
        # Run info dictionary
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
        # AG info dictionary
        'natom': natom,
        'initx': initx,
        'initp': initp,
        'initj': initj,
        'ezeroi': ezeroi,
        'lbinsamp': lbinsamp,
        'sampfilexx': sampfilexx,
        'sampfilepp': sampfilepp,
        'lems': lems,
        'geom': geom,
        'temp0im': temp0im,
        'escale0im': escale0im,
        'samptarg': samptarg,
        'letot': letot,
        'sampjmin': sampjmin,
        'sampjmax': sampjmax,
        'sampjtemp1': sampjtemp1,
        'sampjtemp2': sampjtemp2,
        'sampjbrot1': sampjbrot1,
        'sampjbrot2': sampjbrot2,
        'ejsc1': ejsc1,
        'ejsc2': ejsc2,
        'ejsc3': ejsc3,
        'ejsc4': ejsc4,
        # Collision dictionary
        'bath': bath,
        'iorient': iorient,
        'ldofrag': ldofrag,
        'termflag': termflag,
        'tnstep': tnstep,
        'tgradmag': tgradmag,
        'ioutput': ioutput,
        'ilist': ilist
    }

    return build_mako_str(
        template_file_name='dint_traj.mako',
        template_src_path=TEMPLATE_PATH,
        template_keys=inp_keys)

### WIP
def submission_script(template_name, exe_path, run_dir):
    """ launches the DiNT job """

    # Write the bottom of the string
    job_lines = '# Run several dint instances\n'
    job_lines += 'cd {0}/run1\n'.format(run_dir)
    job_lines += 'time $DINTEXE < dint.inp > output.dat &\n'
#    for i in range(njobs-1):
#        job_lines += 'cd ../run{0}\n'.format(str(i+2))
#        job_lines += 'time $DINTEXE < dint.inp > output.dat &\n'
    job_lines += 'wait\n'

    # Set the dictionary for the DiNT input file
    exe_keys = {
        "exe_path": exe_path,
        "job_lines": job_lines
    }

    return build_mako_str(
        template_file_name=template_name,
        template_src_path=TEMPLATE_PATH,
        template_keys=exe_keys)
