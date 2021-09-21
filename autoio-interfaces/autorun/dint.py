""" autorun functions to do the dintmom.pl script

    STEPS:
        (1) optimize geometry
        (2) sample initial coords of the unimol species
        (3) calculate lj params with OneDMin
        (4) run collision trajectories
        (5) calc moms

    Auxiliary input:
        from PIPPy: coef.dat, basis.dat
        made by hand: tinker files
"""

import os
import automol.geom
import onedmin
import dint_io
import onedmin_io
from autorun._run import from_input_string

# Name of input and output files
INPUT_NAME = 'dint.inp'
OUTPUT_NAMES = ('dint.geo','dint.samp','dint.traj')

# autorun functions
def read_input(run_dir, input_name):
    """ Read in input parameters for dintmom job, runs series of
        DiNT jobs.
        Currently supports:
            Optimization, Sampling, Collision trajectories


    """

def read_dint_input(run_dir, input_name):
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
            UseCL=EXEC_DCT['UseCL'],
            CommandLine=EXEC_DCT['CommandLine']
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
            UseCL=EXEC_DCT['UseCL'],
            CommandLine=EXEC_DCT['CommandLine']
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
            UseCL=EXEC_DCT['UseCL'],
            CommandLine=EXEC_DCT['CommandLine']
        )
    else:
        print('Error: Job Type not supported')
        sys.exit()

    return INP_STR, JOB_TYPE


def optimization(run_dir, exe_path, geofile, basis_str, coef_str):
    """ Optimize the geometry using DiNT.
        1. Read in unoptimized geo from xyz file
        2. Run dint.inp to get dint.geo
    """

    aux_dct = {
        "basis.dat": basis_str,
        "coef.dat": coef_str
#        'tinker.xyz': tinker_xyz
    }

    input_name = 'dint.inp'
    output_names = ('dint.geo','fort.77')
    nprocs = 36 # Bebop

    #$cwd = pwd;
    #chdir $cwd/opt;

    # Read Python input file to create dictionaries
    inp_str, job_type = read_dint_input(run_dir, input_name=input_name)

    assert job_type == 'Opt'

    # Create Fortran opt input file from dictionaries
    input_str = dint_io.writer.opt_input(inp_str)

    # Create submission script
    script_str = dint_io.writer.submission_script(nprocs, run_dir, exe_path, 
                                                dint_in=input_name, dint_out=output_names[0])

    # Run DiNT, generate dint.geo
    output_strs = direct(script_str, run_dir, input_str,
                         aux_dct=aux_dct,
                         input_name=input_name,
                         output_names=output_names)

    #cp dint.geo ..
    #chdir $cwd
    
    if os.file.exists('dint.geo'):
        print('Geometry optimized!')
    else:
        print('Geometry optimization failed -- no dint.geo file was found!')
        sys.exit()

    # Parse values from dint.geo
    energy = dint_io.parser.energy(output_strs)
    rot_consts = dint_io.parser.rot_consts(output_strs)
    opt_geo = dint_io.parser.geo(output_strs)

    return energy, rot_consts, opt_geo


def sampling(run_dir, exe_path, geofile, basis_str, coef_str):
    """ Sample the initial coordinates.
        1. Read in optimized geometry from dint.geo
        2. Run dint.inp for several geoms to get xyz.dat
    """

    aux_dct = {
        'basis.dat': basis_str,
        'coef.dat': coef_str
#        # 'tinker.xyz': tinker_xyz
    }

    input_name='dint.inp'
    output_names=('xyz.dat','fort.80','fort.81')
    nprocs = 36 # Bebop

    # Read Python input file to create dictionaries
    inp_str, job_type = read_dint_input(run_dir, input_name=input_name)

    assert job_type == 'Samp'

    # Create Fortran sampling input file from dictionaries
    input_str = dint_io.writer.samp_input(inp_str)

    # Create submission script
    script_str = dint_io.writer.submission_script(nprocs, run_dir, exe_path, 
                                                dint_in=input_name, dint_out=output_names[0])

    # Run DiNT, generate dint.samp
    output_strs = direct(script_str, run_dir, input_str,
                         aux_dct=aux_dct,
                         input_name=input_name,
                         output_names=output_names)

    return

def brot(run_dir):
    """ 1. Check for a dint.brot file
        2. Generate dint.brot with brot.x from fort.80 if missing
        3. Read rotational constants from dint.brot
    """

    if os.path.exists('dint.brot'):
        print("Found dint.brot")
    else:
        #chdir "$cwd/samp"
        if os.file.exists('fort.80'):
            print("No dint.brot found. Running brot.x")
            script_str = dint_io.writer.submission_script(nprocs, run_dir, exe_path, 
                                dint_in=input_name, dint_out=output_names[0])
            output_strs = direct(script_str, run_dir, input_str,
                                aux_dct=aux_dct,
                                input_name=input_name,
                                output_names=output_names)
        else:
            print('Couldn\'t find sampled fort.80, exiting')
            sys.exit()
        
        #qx ! cp dint.brot ..\/. !;
        #chdir "$cwd" ;

    rot_consts = dint_io.parser.rot_consts(output_names)

    return rot_consts

def calculate_lj():
    """ Run OneDMin to get LJ params
    """

    onedmin_io.lennard_jones_params(sp_script_str, run_dir, nsamp, njobs,
                                    tgt_geo, bath_geo, thy_info, charge, mult,
                                    smin=2.0, smax=6.0, spin_method=1, ranseeds=None)

    return NotImplementedError


def collision_trajectory(run_dir, exe_path, geofile, basis_str, coef_str, 
                         dint_geo, dint_brot, dint_lj):
    """ Trajectory simulations
        1. Read in optimized geo from dint.geo
        2. Read in brot values from dint.brot
        3. Read in LJ values from dint.lj
        4. Run dint.inp to get dint.traj
    """

    aux_dct = {
        'basis.dat': basis_str,
        'coef.dat': coef_str,
        'dint.geo': dint_geo,
        'dint.brot': dint_brot,
        'dint.lj': dint_lj
#        # 'tinker.xyz': tinker_xyz
    }

    input_name='dint.inp'
    output_names=('dint.traj','fort.31')
    nprocs = 36 # Bebop

    inp_str, job_type = read_dint_input(run_dir, input_name=input_name)

    assert job_type == 'Traj'

    # Create Fortran trajectory input file from dictionaries
    input_str = dint_io.writer.traj_input(inp_str)

    # Create submission script
    script_str = dint_io.writer.submission_script(nprocs, run_dir, exe_path, 
                                                dint_in=input_name, dint_out=output_names[0])

    # Run DiNT, generate dint.traj
    output_strs = direct(script_str, run_dir, input_str,
                         aux_dct=aux_dct,
                         input_name=input_name,
                         output_names=output_names)

    return NotImplementedError


def moments():
    """ Moments
        1. Run mom.x by reading in dint.traj
        2. Get rotationally averaged moments from mom.out
    """

    direct()

    moment1 = 
    moment2 = 

    return moment1, moment2


def alpha_calc(run_dir, exe_path, geofile, basis_str, coef_str):
    """ Combines optimization, sampling, brot, calculate_lj, 
        collision_trajectory, and moments to return
        alpha = <Del E_down>
    """
    # Optimizes geometry and energy
    energy, rot_consts, opt_geo = optimization(run_dir, exe_path,
                                               geofile, basis_str, coef_str)

    # Samples unimolecular species
    sampling(run_dir, exe_path, opt_geo, basis_str, coef_str)

    # Run brot.x to get averaged rotational constants
    brot(fort.80)

    # Run OneDMin to get LJ values
    calculate_lj()

    si = onedmin_io.reader.
    ep = onedmin_io.reader.

    # Use averaged rot consts, LJ values, and optimized min E in collision trajs
    collision_trajectory()

    # Calculate moments (alpha) from trajectory statistics
    moments_out_str = moments()

    alpha = dint_io.parser.alpha(moments_out_str)

    return alpha


def direct(script_str, run_dir, input_str, aux_dct=None,
           input_name=INPUT_NAME,
           output_names=OUTPUT_NAMES):
    """ Runs executable
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