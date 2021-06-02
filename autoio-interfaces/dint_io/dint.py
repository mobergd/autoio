""" Sets up DiNT input
"""

import os
import sys
import subprocess
import ioformat
import dint_io


# Set paths
DRIVE_PATH = os.getcwd()

# Parse the input file into a string
INP_STR = ioformat.pathtools.read_file(
    DRIVE_PATH, 'dint.inp', remove_comments='#', remove_whitespace=True)

print('Parsing DiNT input...')
RUN_DCT, AG_DCT, COLL_DCT, EXEC_DCT = dint_io.parser.input_file(INP_STR)

# Job type
JOB_TYPE = RUN_DCT['JobType']

# Write input file
print('Writing to Fortran input file ...')

if JOB_TYPE == 'Opt':
    OPT_INP_STR = dint_io.writer.opt_inp(
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
        natom=AG_DCT['natom'],
        initx=AG_DCT['INITx'],
        initp=AG_DCT['INITp'],
        initj=AG_DCT['INITj'],
        ezeroi=AG_DCT['ezeroi'],
        geom=AG_DCT['geom'],
        termflag=COLL_DCT['TERMFLAG'],
        tnstep=COLL_DCT['tnstep'],
        tgradmag=COLL_DCT['tgradmag'],
        ioutput=COLL_DCT['ioutput'],
        ilist=COLL_DCT['ilist']
    )
elif JOB_TYPE == 'Samp':
    SAMP_INP_STR = dint_io.writer.samp_inp(
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
        natom=AG_DCT['natom'],
        initx=AG_DCT['INITx'],
        initp=AG_DCT['INITp'],
        initj=AG_DCT['INITj'],
        ezeroi=AG_DCT['ezeroi'],
        geom=AG_DCT['geom'],
        temp0im=AG_DCT['temp0im'],
        escale0im=AG_DCT['escale0im'],
        samptarg=AG_DCT['samptarg'],
        sampjmin=AG_DCT['sampjmin'],
        sampjmax=AG_DCT['sampjmax'],
        sampjtemp1=AG_DCT['sampjtemp1'],
        sampjtemp2=AG_DCT['sampjtemp2'],
        sampbrot1=AG_DCT['sampbrot1'],
        sampbrot2=AG_DCT['sampbrot2'],
        termflag=COLL_DCT['TERMFLAG'],
        tnstep=COLL_DCT['tnstep'],
        ioutput=COLL_DCT['ioutput'],
        ilist=COLL_DCT['ilist']
    )
else:
    print('Error: Job Type not supported')
    sys.exit()

ioformat.pathtools.write_file(DINT_INP_STR, DRIVE_PATH, 'input')

# Run Fortran code with new input file if desired
if EXEC_DCT['UseCL'] == 'T':
    print('Running Fortran code ...')
    print(EXEC_DCT['CommandLine'])
    RESULT = subprocess.call(EXEC_DCT['CommandLine'], shell=True)
    if RESULT == 0:
        print('Finished')
    else:
        print('Error: Command Failed')
        sys.exit()
