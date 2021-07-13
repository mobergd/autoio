"""
  Reads the output of a MESS calculation for the
  high-pressure and pressure-dependent rate constants
  corresponding to a given reaction.
"""

import numpy
from phydat import phycon


# Functions for getting k(T,P) values from main MESS `RateOut` file
def ktp_dct(output_str, reactant, product):
    """ Parses the MESS output file string for the rate constants [k(T)]s
        for a single reaction for rate constants at all computed pressures,
        including the high-pressure limit.

        Pressures in atm.
        K(T)s in cm3/mol.s [bimol] or 1/s [unimol]

        :param output_str: string of lines of MESS output file
        :type output_str: str
        :param reactant: label for the reactant used in the MESS output
        :type reactant: str
        :param product: label for the product used in the MESS output
        :type product: str
        :rtype dict[float: (float, float)]
    """

    # Build the reaction string found in the MESS output
    reaction = _reaction_header(reactant, product)

    # Get the MESS output lines
    out_lines = output_str.splitlines()

    # Initialized dictionary with high-pressure rate constants
    _ktp_dct = {'high': _highp_kts(out_lines, reaction)}

    # Read the pressures and convert them to atm if needed
    _pressures, _ = pressures(output_str, mess_file='out')

    # Update the dictionary with the pressure-dependend rate constants
    for pressure in (_press for _press in _pressures if _press != 'high'):
        _ktp_dct.update(
            _pdep_kts(out_lines, reaction, pressure)
        )

    return _ktp_dct


def _highp_kts(out_lines, reaction):
    """ Parses the MESS output file string for the rate constants [k(T)]s
        for a single reaction at the high-pressure limit.

        :param out_lines: all of the lines of MESS output
        :type out_lines: list(str)
        :param reaction: string matching reaction line in MESS output
        :type reaction: str
        :return rate_constants: all high-P rate constants for the reaction
        :rtype list(float)
    """

    # Find where the block of text where the high-pressure rates exist
    block_str = ('High Pressure Rate Coefficients ' +
                 '(Temperature-Species Rate Tables):')
    for i, line in enumerate(out_lines):
        if block_str in line:
            block_start = i
            break

    # Get the high-pressure rate constants
    rate_constants = []
    for i in range(block_start, len(out_lines)):
        if reaction in out_lines[i]:
            rate_const_block_start = i
            rate_constants = _parse_rate_constants(
                out_lines, rate_const_block_start, reaction)
            break

    return rate_constants


def _pdep_kts(out_lines, reaction, pressure):
    """ Parses the MESS output file string for the rate constants [k(T,P)]s
        for a single reaction at a given numerical pressure, P.

        :param out_lines: all of the lines of MESS output
        :type out_lines: list(str)
        :param reaction: string matching reaction line in MESS output
        :type reaction: str
        :param pressure: pressure that k(T,P)s will be read for
        :type pressure: float
        :return rate_constants: k(T,P)s for the reaction at given pressure
        :rtype list(float)
    """

    # Find where the block of text where the pressure-dependent rates exist
    block_str = ('Temperature-Species Rate Tables:')

    pdep_dct = {}
    for i, line in enumerate(out_lines):
        if block_str in line:
            for j in range(i, len(out_lines)):
                if 'Temperature-Pressure Rate Tables' in out_lines[j]:
                    break
                if reaction in out_lines[j]:
                    mess_press = float(out_lines[j-2].strip().split()[2])
                    mess_punit = out_lines[j-2].strip().split()[3]
                    if numpy.isclose(mess_press, pressure):
                        conv_pressure = _convert_pressure(pressure, mess_punit)
                        pdep_dct[conv_pressure] = _parse_rate_constants(
                            out_lines, j, reaction)
                        break

    return pdep_dct


def _parse_rate_constants(out_lines, block_start, reaction):
    """ Parses specific rate constants from the correct column
        in the MESS output file string.

        :param out_lines: all of the lines of MESS output
        :type out_lines: list(str)
        :param block_start: line num corresponding to reaction and pressure
        :type block_start: int
        :param reaction: string matching reaction line in MESS output
        :type reaction: str
        :return rate_constants: all rate constants for the reaction
        :rtype: list(str, float)
    """

    # Find the column corresponding to the reaction
    reaction_col = 0
    reaction_headers = out_lines[block_start].strip().split()
    for i, reaction_header in enumerate(reaction_headers):
        if reaction == reaction_header:
            reaction_col = i
            break

    # Parse the following lines and store the constants in a list
    temps, kts = [], []
    for i in range(block_start+1, len(out_lines)):
        if out_lines[i].strip() == '':
            break
        temps.append(out_lines[i].strip().split()[0])
        kts.append(out_lines[i].strip().split()[reaction_col])

    # Convert temps and rate constants to floats and combine values
    # only do so if the rate constant is defined (i.e., not '***')
    fin_temps = tuple(float(temp) for temp in temps)
    fin_kts = ()
    for kt_i in kts:
        new_kt = float(kt_i) if kt_i != '***' else None
        fin_kts += (new_kt,)

    return (fin_temps, fin_kts)


# Functions for getting k(E) values from main MESS `MicroRateOut` file
def ke_dct(output_str, reactant, product):
    """ Parses the MESS output file string for the microcanonical
        rate constants [k(E)]s for a single reaction.

        :param output_str: string of lines of MESS output file
        :type output_str: str
        :param reactant: label for the reactant used in the MESS output
        :type reactant: str
        :param product: label for the product used in the MESS output
        :type product: str
        :return rate_constants: all high-P rate constants for the reaction
        :rtype dict[float: float]
    """

    # Form string for reaction header using reactant and product name
    reaction = _reaction_header(reactant, product)

    # Break up the file into lines
    out_lines = output_str.split('\n')

    # Determine col idx where reaction is
    head = out_lines[0].replace('E, kcal/mol', 'E').replace('D, mol/kcal', 'D')
    headers = head.split()
    col_idx = headers.index(reaction)

    _ke_dct = {0.0: 0.0}
    for i, line in enumerate(out_lines):
        if i not in (0, 1):
            tmp = line.strip().split()
            if tmp:
                _ke_dct[float(tmp[0])] = float(tmp[col_idx])

    return _ke_dct


# Functions to read temperatures and pressures
def temperatures(file_str, mess_file='out'):
    """ Get temps
    """

    if mess_file == 'out':
        temps = _temperatures_output_string(file_str)
    elif mess_file == 'inp':
        temps = _temperatures_input_string(file_str)
    else:
        temps = ()

    return temps


def pressures(file_str, mess_file='out'):
    """ Get pressures
    """

    if mess_file == 'out':
        _pressures = _pressures_output_string(file_str)
    elif mess_file == 'inp':
        _pressures = _pressures_input_string(file_str)
    else:
        _pressures = ()

    return _pressures


def _temperatures_input_string(input_str):
    """ Reads the temperatures from the MESS input file string
        that were used in the master-equation calculation.
        :param input_str: string of lines of MESS input file
        :type input_str: str
        :return temperatures: temperatures in the input
        :rtype: list(float)
        :return temperature_unit: unit of the temperatures in the input
        :rtype: str
    """

    # Get the MESS input lines
    mess_lines = input_str.splitlines()
    for line in mess_lines:
        if 'TemperatureList' in line:
            temps = tuple(float(val) for val in line.strip().split()[1:])
            temp_unit = line.strip().split('[')[1].split(']')[0]
            break

    return temps, temp_unit


def _temperatures_output_string(output_str):
    """ Reads the temperatures from the MESS output file string
        that were used in the master-equation calculation.
        :param output_str: string of lines of MESS output file
        :type output_str: str
        :return temperatures: temperatures in the output
        :rtype: list(float)
        :return temperature_unit: unit of the temperatures in the output
        :rtype: str
    """

    # Get the MESS output lines
    mess_lines = output_str.splitlines()

    # Find the block of lines where the temperatures can be read
    temp_str = 'Pressure-Species Rate Tables:'
    for i, line in enumerate(mess_lines):
        if temp_str in line:
            block_start = i
            break

    # Read the temperatures
    temps = []
    for i in range(block_start, len(mess_lines)):
        if 'Temperature =' in mess_lines[i]:
            tmp = mess_lines[i].strip().split()
            temps.append(float(tmp[2]))
    temps = list(set(temps))
    temps.sort()

    # Read unit
    for i in range(block_start, len(mess_lines)):
        if 'Temperature =' in mess_lines[i]:
            temp_unit = mess_lines[i].strip().split()[3]
            break

    return tuple(temps), temp_unit


def _pressures_input_string(input_str):
    """ Reads the pressures from the MESS input file string
        that were used in the master-equation calculation.
        :param input_str: string of lines of MESS input file
        :type input_str: str
        :return pressures: pressures in the input
        :rtype: list(str, float)
        :return pressure_unit: unit of the pressures in the input
        :rtype: str
    """

    # Get the MESS input lines
    mess_lines = input_str.splitlines()
    for line in mess_lines:
        if 'PressureList' in line:
            _pressures = [float(val) for val in line.strip().split()[1:]]
            pressure_unit = line.strip().split('[')[1].split(']')[0]
            break

    # Append high pressure
    _pressures.append('high')

    return tuple(_pressures), pressure_unit


def _pressures_output_string(output_str):
    """ Reads the pressures from the MESS output file string
        that were used in the master-equation calculation.
        :param output_str: string of lines of MESS output file
        :type output_str: str
        :return pressures: pressures in the output
        :rtype: list(str, float)
        :return pressure_unit: unit of the pressures in the output
        :rtype: str
    """

    # Get the MESS output lines
    mess_lines = output_str.splitlines()

    # Find the block of lines where the pressures can be read
    pressure_str = 'Pressure-Species Rate Tables:'
    for i, line in enumerate(mess_lines):
        if pressure_str in line:
            block_start = i
            break

    # Read the pressures
    _pressures = []
    for i in range(block_start, len(mess_lines)):
        if 'P(' in mess_lines[i]:
            pressure_unit = mess_lines[i].strip().split('(')[1].split(')')[0]
            pressure_start = i+1
            for j in range(pressure_start, len(mess_lines)):
                if 'O-O' in mess_lines[j]:
                    break
                tmp = mess_lines[j].strip().split()
                _pressures.append(float(tmp[0]))
            break

    # Append high pressure
    _pressures.append('high')

    return tuple(_pressures), pressure_unit


def _convert_pressure(pressure, pressure_unit):
    """ Convert a set of pressures using the pressure unit, accounting
        for high-pressure in list

        :param pressure: pressures to convert
        :type pressure: tuple(float, str)
        :param pressure_unit: unit of pressures
        :type pressure_unit: str
        :rtype: tuple(float, str)
    """

    if pressure != 'high':
        if pressure_unit == 'atm':
            conv = 1.0
        elif pressure_unit == 'torr':
            conv = phycon.TORR2ATM
        elif pressure_unit == 'bar':
            conv = phycon.BAR2ATM
        pressure *= conv

    return pressure


# Read the labels for all species and reactions
def reactions(out_str, read_fake=False, read_self=False, read_rev=True):
    """ Read the reactions from the output file.

        Ignores 'Capture' reactions
    """

    # Read all of the reactions out of the file
    rxns = ()
    for line in out_str.splitlines():
        if 'T(K)' in line and '->' in line:
            rxns += tuple(line.strip().split()[1:])

    # Remove duplcates while preserving order
    rxns = tuple(n for i, n in enumerate(rxns) if n not in rxns[:i])

    # Remove capture reactions
    rxns = tuple(rxn for rxn in rxns if rxn != 'Capture')

    # Build list of reaction pairs: rct->prd = (rct, prd)
    # Filter out reaction as necessary
    rxn_pairs = ()
    for rxn in rxns:
        [rct, prd] = rxn.split('->')
        if not read_fake:
            if 'F' in rxn or 'B' in rxn:
                continue
        if not read_self:
            if rct == prd:
                continue
        if prd:  # removes rct->  reactions in output
            rxn_pairs += ((rct, prd),)

    # Remove reverse reactions, if requested
    if read_rev:
        sort_rxn_pairs = rxn_pairs
    else:
        sort_rxn_pairs = ()
        for pair in rxn_pairs:
            rct, prd = pair
            if (rct, prd) in sort_rxn_pairs or (prd, rct) in sort_rxn_pairs:
                continue
            sort_rxn_pairs += ((rct, prd),)

    return sort_rxn_pairs


def labels(file_str, read_fake=False, mess_file='out'):
    """ Read the labels out of a MESS file
    """

    if mess_file == 'out':
        lbls = _labels_output_string(file_str)
    elif mess_file == 'inp':
        lbls = _labels_input_string(file_str)
    else:
        lbls = ()

    if not read_fake:
        lbls = tuple(lbl for lbl in lbls
                     if 'F' not in lbl and 'f' not in lbl)

    return lbls


def _labels_input_string(inp_str):
    """ Read the labels out of a MESS input file
    """

    def _read_label(line, header):
        """ Get a labe from a line
        """
        lbl = None
        idx = 2 if header != 'Barrier' else 4
        line_lst = line.split()
        if len(line_lst) == idx and '!' not in line:
            lbl = line_lst[idx]
        return lbl

    lbls = ()
    for line in inp_str.splitlines():
        if 'Well ' in line:
            lbls += (_read_label(line, 'Well'),)
        elif 'Bimolecular ' in line:
            lbls += (_read_label(line, 'Bimolecular'),)
        elif 'Barrier ' in line:
            lbls += (_read_label(line, 'Barrier'),)

    return lbls


def _labels_output_string(out_str):
    """ Read the labels out of a MESS input file
    """

    lbls = []
    for line in out_str.splitlines():
        if 'T(K)' in line and '->' not in line:
            rxns = line.strip().split()[1:]
            line_lbls = [rxn.split('->') for rxn in rxns]
            line_lbls = [lbl for sublst in line_lbls for lbl in sublst]
            lbls.extend(line_lbls)

    # Remove duplicates and make lst a tuple
    lbls = tuple(set(lbls))

    return lbls


# Helper functions
def _reaction_header(reactant, product):
    return reactant + '->' + product
