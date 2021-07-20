""" autorun functions to do the dintmom.pl script

    STEPS:
        (1) optimize geometry
        (2) sample initial coords of the unimol spc
        (3) calculate lj params
        (4) run collision trajectories
        (5) calc moms

    Auxiliary input:
        from PIPPy: coef.dat, basis.dat
        made by hand?: tinker files
"""

import os
import automol.geom
import autorun.onedmin
import dint_io
import onedmin_io
from autorun._run import from_input_string

# Name of input and output files
INPUT_NAME = 'dint.inp'
OUTPUT_NAMES = ('dint.opt','dint.samp','dint.traj')

# autorun functions
def read_input(run_dir, input_name):
    """ Read in input parameters for different DiNT jobs
        Currently supports:
            Optimization, Sampling, Collision trajectories

        :param sp_script_str: submission script for DiNT job
        :type sp_script_str: str
        :param run_dir: directory where all DiNT jobs are run
        :type run_dir: str
        :param input_str: list of input variables to read and interpret
        :type input_str: str
        :param aux_dct: auxiliary dictionary for other inputs
        :type aux_dct: str
        :param input_name: name of DiNT input file
        :type input_name: str
        :param output_names: name(s) of DiNT output files (dint.xxx, fort.xx)
        :type output_names: str
    """

    print('Parsing DiNT input...')
    inp = os.path.join(run_dir, input_name)
    RUN_DCT, AG_DCT, COLL_DCT, EXEC_DCT = dint_io.parser.input_file(inp)

    JOB_TYPE = RUN_DCT['JobType']

    if JOB_TYPE == 'Opt':
        print('Job type: Optimization')
        INP_STR = dint_io.writer.opt_input(
            # Run info dictionary
            potflag=RUN_DCT['POTFLAG'],
            nsurf0=RUN_DCT['nsurf0'],
            nsurft=RUN_DCT['nsurft'],
            methflag=RUN_DCT['METHFLAG'],
            repflag=RUN_DCT['REPFLAG'],
            intflag=RUN_DCT['INTFLAG'],
            hstep0=RUN_DCT['hstep0'],
            eps=RUN_DCT['eps'],
            nprint=RUN_DCT['nprint'],
            ranseed=RUN_DCT['ranseed'],
            ntraj=RUN_DCT['ntraj'],
            tflag1=RUN_DCT['TFLAG1'],
            tflag2=RUN_DCT['TFLAG2'],
            tflag3=RUN_DCT['TFLAG3'],
            tflag4=RUN_DCT['TFLAG4'],
            nmol=RUN_DCT['nmol'],
            ezero=RUN_DCT['ezero'],
            # AG info dictionary
            natom=AG_DCT['natom'],
            initx=AG_DCT['INITx'],
            initp=AG_DCT['INITp'],
            initj=AG_DCT['INITj'],
            ezeroi=AG_DCT['ezeroi'],
            geom=AG_DCT['geom'],
            # Collision dictionary
            termflag=COLL_DCT['TERMFLAG'],
            tnstep=COLL_DCT['tnstep'],
            tgradmag=COLL_DCT['tgradmag'],
            ioutput=COLL_DCT['ioutput'],
            ilist=COLL_DCT['ilist'],
            # Execution dictionary
            UseCL=EXEC_DCT['UseCL']
        )
    elif JOB_TYPE == 'Samp':
        print('Job type: Sampling')
        INP_STR = dint_io.writer.samp_input(
            # Run info dictionary
            potflag=RUN_DCT['POTFLAG'],
            nsurf0=RUN_DCT['nsurf0'],
            nsurft=RUN_DCT['nsurft'],
            methflag=RUN_DCT['METHFLAG'],
            repflag=RUN_DCT['REPFLAG'],
            intflag=RUN_DCT['INTFLAG'],
            hstep=RUN_DCT['hstep'],
            nprint=RUN_DCT['nprint'],
            ranseed=RUN_DCT['ranseed'],
            ntraj=RUN_DCT['ntraj'],
            tflag1=RUN_DCT['TFLAG1'],
            tflag2=RUN_DCT['TFLAG2'],
            tflag3=RUN_DCT['TFLAG3'],
            tflag4=RUN_DCT['TFLAG4'],
            nmol=RUN_DCT['nmol'],
            ezero=RUN_DCT['ezero'],
            # AG info dictionary
            natom=AG_DCT['natom'],
            initx=AG_DCT['INITx'],
            initp=AG_DCT['INITp'],
            initj=AG_DCT['INITj'],
            ezeroi=AG_DCT['ezeroi'],
            geom=AG_DCT['geom'],
            temp0im=AG_DCT['temp0im'],
            escale0im=AG_DCT['escale0im'],
            samptarg=AG_DCT['samptarg'],
            letot=AG_DCT['letot'],
            sampjmin=AG_DCT['sampjmin'],
            sampjmax=AG_DCT['sampjmax'],
            sampjtemp1=AG_DCT['sampjtemp1'],
            sampjtemp2=AG_DCT['sampjtemp2'],
            sampjbrot1=AG_DCT['sampjbrot1'],
            sampjbrot2=AG_DCT['sampjbrot2'],
            # Collision dictionary
            termflag=COLL_DCT['TERMFLAG'],
            tnstep=COLL_DCT['tnstep'],
            ioutput=COLL_DCT['ioutput'],
            ilist=COLL_DCT['ilist'],
            # Execution dictionary
            UseCL=EXEC_DCT['UseCL']
        )
    elif JOB_TYPE == 'Traj':
        print('Job type: DiNT Trajectories')
        INP_STR = dint_io.writer.traj_input(
            # Run info dictionary
            potflag=RUN_DCT['POTFLAG'],
            nsurf0=RUN_DCT['nsurf0'],
            nsurft=RUN_DCT['nsurft'],
            methflag=RUN_DCT['METHFLAG'],
            repflag=RUN_DCT['REPFLAG'],
            intflag=RUN_DCT['INTFLAG'],
            hstep=RUN_DCT['hstep'],
            eps=RUN_DCT['eps'],
            nprint=RUN_DCT['nprint'],
            ranseed=RUN_DCT['ranseed'],
            ntraj=RUN_DCT['ntraj'],
            tflag1=RUN_DCT['TFLAG1'],
            tflag2=RUN_DCT['TFLAG2'],
            tflag3=RUN_DCT['TFLAG3'],
            tflag4=RUN_DCT['TFLAG4'],
            nmol=RUN_DCT['nmol'],
            ezero=RUN_DCT['ezero'],
            # AG info dictionary
            natom=AG_DCT['natom'],
            initx=AG_DCT['INITx'],
            initp=AG_DCT['INITp'],
            initj=AG_DCT['INITj'],
            ezeroi=AG_DCT['ezeroi'],
            samptot=AG_DCT['samptot'],
            lbinsamp=AG_DCT['lbinsamp'],
            sampfilexx=AG_DCT['sampfilexx'],
            sampfilepp=AG_DCT['sampfilepp'],
            lems=AG_DCT['lems'],
            geom=AG_DCT['geom'],
            temp0im=AG_DCT['temp0im'],
            escale0im=AG_DCT['escale0im'],
            samptarg=AG_DCT['samptarg'],
            letot=AG_DCT['letot'],
            sampjmin=AG_DCT['sampjmin'],
            sampjmax=AG_DCT['sampjmax'],
            sampjtemp1=AG_DCT['sampjtemp1'],
            sampjtemp2=AG_DCT['sampjtemp2'],
            sampjbrot1=AG_DCT['sampjbrot1'],
            sampjbrot2=AG_DCT['sampjbrot2'],
            ejsc1=AG_DCT['ejsc1'],
            ejsc2=AG_DCT['ejsc2'],
            ejsc3=AG_DCT['ejsc3'],
            ejsc4=AG_DCT['ejsc4'],
            # Collision dictionary
            bath=COLL_DCT['bath'],
            iorient=COLL_DCT['iorient'],
            ldofrag=COLL_DCT['ldofrag'],
            termflag=COLL_DCT['TERMFLAG'],
            tnstep=COLL_DCT['tnstep'],
            ioutput=COLL_DCT['ioutput'],
            ilist=COLL_DCT['ilist'],
            # Execution dictionary
            UseCL=EXEC_DCT['UseCL']
        )
    else:
        print('Error: Job Type not supported')
        sys.exit()

    return INP_STR


def optimization(script_str, run_dir,
                 geo, basis_str, coef_str):
    """ Optimize the geometry using DiNT.
        1. Read in unoptimized geo from xyz file
        2. Run dint.inp to get dint.opt
    """

    aux_dct = {
        'basis.dat': basis_str,
        'coef.dat': coef_str
#        # 'tinker.xyz': tinker_xyz
    }

    input_name='dint.inp'
    output_names=('dint.opt','fort.77')

    script_str=dint_io.writer.submission_script()

    # Read input file to cr
    inp_str = read_input(script_str, run_dir,
                       aux_dct=aux_dct,
                       input_name=input_name,
                       output_names=output_names
                       )

    assert JOB_TYPE is 'Opt'

    # Create opt input file
    input_str = dint_io.writer.opt_input(inp_str)

    # Run DiNT, generate dint.opt
    output_strs = direct(script_str, run_dir, input_str,
                         aux_dct=aux_dct,
                         input_name=input_name,
                         output_names=output_names)

    # Parse values from dint.opt
    energy = dint_io.parser.energy(output_strs)
    rot_consts = dint_io.parser.rot_consts(output_strs)
    opt_geo = dint_io.parser.geo(output_strs)

    return energy, rot_consts, opt_geo


def sampling(script_str, run_dir,
             geo, basis_str, coef_str):
    """ Sample the initial coordinates.
        1. Read in optimized geometry from dint.opt
        2. Run dint.inp for several geoms to get dint.samp
    """

    aux_dct = {
        'basis.dat': basis_str,
        'coef.dat': coef_str
#        # 'tinker.xyz': tinker_xyz
    }

    input_name='dint.inp'
    output_names=('dint.samp','fort.80','fort.81')

    input = read_input(
        script_str, run_dir, input_str,
        aux_dct=aux_dct,
        input_name=INPUT_NAME,
        output_names=output_names
    )

    # Create sampling input file
    dint_io.writer.samp_input(input)

    # Run DiNT, generate dint.samp
    output_strs = direct(script_str, run_dir, input_str,
                         aux_dct=aux_dct,
                         input_name=input_name,
                         output_names=output_names)

    # Parse values from dint.samp

    return

def brot():
    """ 1. Check for a dint.brot file
        2. Generate dint.brot with brot.x from fort.80 if missing
        3. Read rotational constants from dint.brot
    """

    if os.path.exists('dint.brot'):
        print("Found dint.brot")
    else:
        print("No dint.brot. Running brot.x")
        input_strs = read_input(
            script_str, run_dir, input_str,
            input_name='fort.80',
            output_names=('dint.brot')
        )

    rot_consts = dint_io.parser.rot_consts(output_names)

    return NotImplementedError

def calculate_lj():
    """ Run OneDMin to get LJ params
    """
    onedmin_io.direct(
    )
    onedmin_io.lennard_jones_params(
    )

    return NotImplementedError


def collision_trajectory():
    """ Trajectory simulations
        1. Read in optimized geo from dint.geo
        2. Read in brot values from dint.brot
        3. Read in LJ values from dint.lj
        4. Run dint.inp to get dint.traj
    """
    input = read_input(
        script_str, run_dir, input_str,
        aux_dct=aux_dct,
        input_name=INPUT_NAME,
        output_names=('dint.traj','fort.31')
    )

    aux_dct = {
        'basis.dat': basis_str,
        'coef.dat': coef_str,
        'dint.geo': dint.geo,
        'dint.brot': dint.brot,
        'dint.lj': dint.lj
#        # 'tinker.xyz': tinker_xyz
    }

    dint_io.writer.traj_input(input)

    return NotImplementedError


def moments():
    """ Moments
        1. Run mom.x by reading in dint.traj
        2. Get rotationally averaged moments from mom.out
    """

    moment1 = 
    moment2 = 

    return moment1, moment2


def alpha_calc():
    """ Combines optimization, sampling, calculate_lj, 
        collision_trajectory, and moments to return
        alpha = <Del E_down>
    """



    si = onedmin_io.reader.
    ep = onedmin_io.reader.
    zlj = onedmin_io.reader.

    alpha = dint_io.reader.summary(output_str)

    return alpha


def direct(script_str, run_dir, input_str, aux_dct=None,
           input_name=INPUT_NAME,
           output_names=OUTPUT_NAMES):
    """
        :param aux_dct: auxiliary input strings dict[name: string]
        :type aux_dct: dict[str: str]
        :param script_str: string of bash script that contains
            execution instructions electronic structure job
        :type script_str: str
        :param run_dir: name of directory to run electronic structure job
        :type run_dir: str
    """
    output_strs = from_input_string(
        script_str, run_dir, input_str,
        aux_dct=aux_dct,
        input_name=input_name,
        output_names=output_names)

    return output_strs