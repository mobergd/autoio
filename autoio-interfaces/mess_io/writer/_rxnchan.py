"""
Writes MESS input for a molecule
"""

import os
from ioformat import build_mako_str
from mess_io.writer import _format as messformat


# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')
SECTION_PATH = os.path.join(TEMPLATE_PATH, 'sections')
RXNCHAN_PATH = os.path.join(SECTION_PATH, 'reaction_channel')


def species(spc_label, spc_data, zero_ene=None):
    """ Writes the string that defines the `Species` section for
        for a given species for a MESS input file by
        formatting input information into strings a filling Mako template.

        :param spc_label: label for input species used by MESS
        :type spc_label: str
        :param spc_data: MESS string with required electronic structure data
        :type spc_data: str
        :param zero_ene: elec+zpve energy relative to PES reference
        :rtype: str
    """

    # Indent the string containing all of data for the well
    spc_data = messformat.indent(spc_data, 2)

    # Format the precision of the zero energy
    if zero_ene is not None:
        zero_ene = '{0:<8.2f}'.format(zero_ene)

    # Create dictionary to fill template
    spc_keys = {
        'spc_label': spc_label,
        'spc_data': spc_data,
        'zero_ene': zero_ene
    }

    return build_mako_str(
        template_file_name='species.mako',
        template_src_path=RXNCHAN_PATH,
        template_keys=spc_keys)


def well(well_label, well_data,
         zero_ene=None, well_cap=None,
         edown_str=None, collid_freq_str=None):
    """ Writes the string that defines the `Well` section for
        for a given species for a MESS input file by
        formatting input information into strings a filling Mako template.

        :param well_label: label for input well used by MESS
        :type well_label: str
        :param well_data: MESS string with required electronic structure data
        :type well_data: str
        :param zero_ene: elec+zpve energy relative to PES reference
        :type zero_ene: float
        :param well_cap: value for the well extension cap keyword
        :type well_cap: float
        :param edown_str: String for the energy down parameters
        :type edown_str: str
        :param collid_freq_str: String for the collisional freq parameters
        :type collid_freq_str: str
        :rtype: str
    """

    # Indent the string containing all of data for the well
    well_data = messformat.indent(well_data, 4)

    # Format the precision of the zero energy and well extension cap
    if zero_ene is not None:
        zero_ene = '{0:<8.2f}'.format(zero_ene)
    if well_cap is not None:
        well_cap = '{0:<8.2f}'.format(well_cap)

    # Indent the energy transfer parameter strings if needed
    if edown_str is not None:
        edown_str = messformat.indent(edown_str, 4)
    if collid_freq_str is not None:
        collid_freq_str = messformat.indent(collid_freq_str, 4)

    # Create dictionary to fill template
    well_keys = {
        'well_label': well_label,
        'well_data': well_data,
        'zero_ene': zero_ene,
        'well_cap': well_cap,
        'edown_str': edown_str,
        'collid_freq_str': collid_freq_str
    }

    return build_mako_str(
        template_file_name='well.mako',
        template_src_path=RXNCHAN_PATH,
        template_keys=well_keys)


def bimolecular(bimol_label,
                species1_label, species1_data,
                species2_label, species2_data,
                ground_energy):
    """ Writes a Bimolecular section.
    """

    # Indent the string containing all of data for each species
    species1_data = messformat.indent(species1_data, 4)
    species2_data = messformat.indent(species2_data, 4)

    # Determine if species is an atom
    isatom1 = messformat.is_atom_in_str(species1_data)
    isatom2 = messformat.is_atom_in_str(species2_data)

    # Format the precision of the ground energy
    ground_energy = '{0:<8.2f}'.format(ground_energy)

    # Create dictionary to fill template
    bimol_keys = {
        'bimolec_label': bimol_label,
        'species1_label': species1_label,
        'species1_data': species1_data,
        'isatom1': isatom1,
        'species2_label': species2_label,
        'species2_data': species2_data,
        'isatom2': isatom2,
        'ground_energy': ground_energy
    }

    return build_mako_str(
        template_file_name='bimolecular.mako',
        template_src_path=RXNCHAN_PATH,
        template_keys=bimol_keys)


def ts_sadpt(ts_label, reac_label, prod_label, ts_data,
             zero_ene=None, tunnel=''):
    """ Writes the string that defines the `Barrier` section for
        for a given transition state, modeled as a PES saddle point,
        for fixed transition state theory. MESS input file string built by
        formatting input information into strings a filling Mako template.

        :param ts_label: label for input TS used by MESS
        :type ts_label: str
        :param reac_label: label for reactant connected to TS used by MESS
        :type reac_label: str
        :param prod_label: label for product connected to TS used by MESS
        :type prod_label: str
        :param ts_data: MESS string with required electronic structure data
        :type ts_data: str
        :param zero_ene: elec+zpve energy relative to PES reference
        :type zero_ene: float
        :param tunnel: `Tunnel` section MESS-string for TS
        :type tunnel: str
        :rtype: str
    """

    # Indent the string containing all of data for the saddle point
    ts_data = messformat.indent(ts_data, 2)
    if tunnel != '':
        tunnel = messformat.indent(tunnel, 4)

    # Format the precision of the zero energy
    if zero_ene is not None:
        zero_ene = '{0:<8.2f}'.format(zero_ene)

    # Create dictionary to fill template
    ts_sadpt_keys = {
        'ts_label': ts_label,
        'reac_label': reac_label,
        'prod_label': prod_label,
        'ts_data': ts_data,
        'zero_ene': zero_ene,
        'tunnel': tunnel
    }

    return build_mako_str(
        template_file_name='ts_sadpt.mako',
        template_src_path=RXNCHAN_PATH,
        template_keys=ts_sadpt_keys)


def ts_variational(ts_label, reac_label, prod_label, rpath_strs,
                   zero_enes=None, tunnel=''):
    """ Writes the string that defines the `Barrier` section for
        for a given transition state, modeled using points along reaction path,
        for varational transition state theory. MESS input file string built by
        formatting input information into strings a filling Mako template.

        :param ts_label: label for input TS used by MESS
        :type ts_label: str
        :param reac_label: label for reactant connected to TS used by MESS
        :type reac_label: str
        :param prod_label: label for product connected to TS used by MESS
        :type prod_label: str
        :param rpath_pt_strs: MESS strings for each point on reaction path
        :type rpath_pt_strs: list(str)
        :param tunnel: `Tunnel` section MESS-string for TS
        :type tunnel: str
        :rtype: str
    """

    assert len(rpath_strs) == len(zero_enes), (
        'Number of rpath strings ({})'.format(len(rpath_strs)),
        'and zero energies ({}) do not match'.format(len(zero_enes))
    )

    # Build the zero energy strings and add them to the rpath strings
    full_rpath_str = ''
    for rpath_str, zero_ene in zip(rpath_strs, zero_enes):
        zero_ene_str = messformat.zero_energy_format(zero_ene)
        zero_ene_str = messformat.indent(zero_ene_str, 2)

        full_rpath_str += rpath_str
        full_rpath_str += zero_ene_str
        full_rpath_str += '\n\n'
        full_rpath_str += 'End  ! RPATH PT\n'

    # Concatenate all of the variational point strings and indent them
    ts_data = messformat.indent(full_rpath_str, 4)
    if tunnel != '':
        tunnel = messformat.indent(tunnel, 4)

    # Create dictionary to fill template
    var_keys = {
        'ts_label': ts_label,
        'reac_label': reac_label,
        'prod_label': prod_label,
        'ts_data': ts_data,
        'tunnel': tunnel
    }

    return build_mako_str(
        template_file_name='ts_var.mako',
        template_src_path=RXNCHAN_PATH,
        template_keys=var_keys)


def dummy(dummy_label, zero_ene=None):
    """ Writes the string that defines the `Dummy` section,
        for dummy reaction products, for a MESS input file by
        formatting input information into strings a filling Mako template.

        :param dummy_label: label for dummy product used by MESS
        :type dummy_label: str
        :rtype: str
    """

    # Format energy string if needed
    if zero_ene is not None:
        zero_ene = '{0:6.2f}'.format(zero_ene)

    # Create dictionary to fill template
    dummy_keys = {
        'dummy_label': dummy_label,
        'zero_ene': zero_ene
    }

    return build_mako_str(
        template_file_name='dummy.mako',
        template_src_path=RXNCHAN_PATH,
        template_keys=dummy_keys)


def configs_union(mol_data_strs, zero_enes, tunnel_strs=None):
    """ Writes the string that defines the `Union` section, containing
        multiple configurations for a given species, for a MESS input file by
        formatting input information into strings a filling Mako template.

        :param mol_data_strs: MESS strings with data for all configurations
        :type mol_data_strs: list(str)
        :rtype: str
    """

    # Build the zero energy strings and add them to the union strings
    union_data = ''
    for idx, (union_str, zero_ene) in enumerate(zip(mol_data_strs, zero_enes)):
        zero_ene_str = messformat.zero_energy_format(zero_ene)
        zero_ene_str = messformat.indent(zero_ene_str, 2)

        union_data += union_str
        union_data += zero_ene_str
        if tunnel_strs is not None:
            _tunnel_str = '\n{}\nEnd  ! Tunnel\n'.format(tunnel_strs[idx])
            union_data += messformat.indent(_tunnel_str, 2)
        union_data += '\n\n'
        union_data += 'End  ! Union{}\n'.format(idx+1)

    # Concatenate all of the molecule strings
    union_data = messformat.indent(union_data, 2)

    # Create dictionary to fill template
    union_keys = {
        'union_data': union_data
    }

    return build_mako_str(
        template_file_name='union.mako',
        template_src_path=RXNCHAN_PATH,
        template_keys=union_keys)
