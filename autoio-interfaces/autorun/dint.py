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

import automol.geom
import dint_io
from autorun._run import from_input_string


INPUT_NAME = 'dint.inp'
OUTPUT_NAMES = ('dint.opt','dint.samp','dint.traj')

# autorun functions
def read_input(script_str, run_dir, input_str,
               aux_dct, input_name, output_names):

    print('Parsing DiNT input...')
#    input_str = dint_io.parser.input_file(INPUT_NAME)
    RUN_DCT, AG_DCT, COLL_DCT, EXEC_DCT = dint_io.parser.input_file(INPUT_NAME)

    JOB_TYPE = RUN_DCT['JobType']

    if JOB_TYPE == 'Opt':
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
            ilist=COLL_DCT['ilist']
        )
    elif JOB_TYPE == 'Samp':
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
            sampbrot1=AG_DCT['sampbrot1'],
            sampbrot2=AG_DCT['sampbrot2'],
            # Collision dictionary
            termflag=COLL_DCT['TERMFLAG'],
            tnstep=COLL_DCT['tnstep'],
            ioutput=COLL_DCT['ioutput'],
            ilist=COLL_DCT['ilist']
        )
    elif JOB_TYPE = 'Traj':
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
            bath
            iorient=COLL_DCT['iorient'],
            ldofrag=COLL_DCT['ldofrag'],
            termflag=COLL_DCT['TERMFLAG'],
            tnstep=COLL_DCT['tnstep'],
            ioutput=COLL_DCT['ioutput'],
            ilist=COLL_DCT['ilist']
        )
        return NotImplementedError
        sys.exit()
    else:
        print('Error: Job Type not supported')
        sys.exit()

    return INP_STR


def optimization(script_str, run_dir,
                 geo, basis_str, coef_str):
    """ Optimize the geometry using DiNT.
    """

    aux_dct = {
        'basis.dat': basis_str,
        'coef.dat': coef_str
#        # 'tinker.xyz': tinker_xyz
    }

    input_strs = read_input(
        script_str, run_dir, input_str,
        aux_dct=aux_dct,
        input_name='dint.inp',
        output_names=('dint.opt','fort.77'))

    # Parse out the info
    opt_geo = dint_io.parser.geo(output_names)
    rot_consts = dint_io.parser.rot_consts(output_names)
    energy = dint_io.parser.energy(output_names)

    ioformat.pathtools.write_file(DINT_INP_STR, DRIVE_PATH, 'input')

    return opt_geo, rot_consts, energy


def sampling(script_str, run_dir,
             geo, basis_str, coef_str):
    """ Sample the initial coordinates.
        run optimized geometries for several geoms
        find a dint.brot file or build from fort.80 with brot.x
    """

    aux_dct = {
        'basis.dat': basis_str,
        'coef.dat': coef_str
#        # 'tinker.xyz': tinker_xyz
    }

    input_strs = read_input(
        script_str, run_dir, input_str,
        aux_dct=aux_dct,
        input_name='dint.inp',
        output_names=('dint.samp','fort.80','fort.81'))

    # Parse out the info

    ioformat.pathtools.write_file(DINT_INP_STR, DRIVE_PATH, 'input')

    return

def calculate_lj():
    """ Run brot.f program
    """
    xyz file
    collide
    return NotImplementedError


def collision_trajectory():
    """ Trajectory simulations
    """
    return NotImplementedError


def moments():
    """ Moments
        # Write param.inc
        # compile mom.x file to get moments
        maybe combine with collsion trajectory calculation
    """

    return NotImplementedError


def direct(script_str, run_dir, input_str, aux_dct=None,
           input_name=INPUT_NAME,
           output_names=OUTPUT_NAMES):
    """
        :param script_str: string of bash script that contains
            execution instructions electronic structure job
        :type script_str: str
        :param run_dir: name of directory to run electronic structure job
        :type run_dir: str
        :param input_writer: elstruct writer module function for desired job
        :type input_writer: elstruct function
        :param aux_dct: auxiliary input strings dict[name: string]
        :type aux_dct: dict[str: str]
    """
    return from_input_string(
        script_str, run_dir, input_str,
        aux_dct=aux_dct,
        input_name=input_name,
        output_names=output_names)
