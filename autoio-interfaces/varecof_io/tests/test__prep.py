""" test automol.varecof_io.writer.prep
"""

import automol
import varecof_io.writer


# C2H6 + H,OH, CH3
CH3CH2_ZMA = (
    ('C', (None, None, None), (None, None, None),
     (None, None, None)),
    ('C', (0, None, None), ('R1', None, None),
     (2.8034554750087315, None, None)),
    ('H', (0, 1, None), ('R2', 'A2', None),
     (2.0477351881268895, 2.0981132181844426, None)),
    ('H', (0, 1, 2), ('R3', 'A3', 'D3'),
     (2.047734870248051, 2.0981200780710814, 3.2899037073022956)),
    ('H', (1, 0, 2), ('R4', 'A4', 'D4'),
     (2.0658681830076175, 1.924883755832615, 1.4966025648868544)),
    ('H', (1, 0, 4), ('R5', 'A5', 'D5'),
     (2.066515824593951, 1.9255815274161476, 2.0975452731245743)),
    ('H', (1, 0, 4), ('R6', 'A6', 'D6'),
     (2.0665179597230052, 1.9255796786166188, 4.185639485867064)))
H_ZMA = (
    ('H', (None, None, None), (None, None, None), (None, None, None)),)
OH_ZMA = (
    ('O', (None, None, None), (None, None, None),
     (None, None, None)),
    ('H', (0, None, None), ('R1', None, None),
     (1.8477888590491485, None, None)))
CH3_ZMA = (
    ('C', (None, None, None), (None, None, None),
     (None, None, None)),
    ('H', (0, None, None), ('R1', None, None),
     (2.04572282078478, None, None)),
    ('H', (0, 1, None), ('R2', 'A2', None),
     (2.045723120545338, 2.0943969516247156, None)),
    ('H', (0, 1, 2), ('R3', 'A3', 'D3'),
     (2.0457228854610228, 2.0943921145330617, 3.1415961306090057)))
CH3CH2_H_ZMA = (
    ('C', (None, None, None), (None, None, None),
     (None, None, None)),
    ('C', (0, None, None), ('R1', None, None),
     (2.857375545788057, None, None)),
    ('H', (0, 1, None), ('R2', 'A2', None),
     (2.067518646663273, 1.929774680570445, None)),
    ('H', (0, 1, 2), ('R3', 'A3', 'D3'),
     (2.067519421597435, 1.92977503072225, 2.0943955639047283)),
    ('H', (0, 1, 2), ('R4', 'A4', 'D4'),
     (2.0675198156854693, 1.9297748255978684, 4.188790396308539)),
    ('H', (1, 0, 2), ('R5', 'A5', 'D5'),
     (2.0675195325608655, 1.9297751281189566, 3.141594868756542)),
    ('H', (1, 0, 5), ('R6', 'A6', 'D6'),
     (2.0675190726592323, 1.9297747755130488, 4.18878925757192)),
    ('H', (1, 0, 5), ('R7', 'A7', 'D7'),
     (10.000, 1.9297750256469979, 2.0943942776405065)))
FRM_KEYS = (1, 7)
CH3CH2_OH_ZMA = ()
CH3CH2_CH3_ZMA = ()


def test__constraint():
    """ test varecof_io.writer.intramolecular_constraint_dct
    """

    ref_const_dct = {
        'R1': 2.857375545788057,
        'R2': 2.067518646663273,
        'A2': 1.929774680570445,
        'R3': 2.067519421597435,
        'A3': 1.92977503072225,
        'D3': 2.0943955639047283,
        'R4': 2.0675198156854693,
        'A4': 1.9297748255978684,
        'D4': 4.188790396308539,
        'R5': 2.0675195325608655,
        'A5': 1.9297751281189566,
        'D5': 3.141594868756542,
        'R6': 2.0675190726592323,
        'A6': 1.9297747755130488,
        'D6': 4.18878925757192}

    const_dct = varecof_io.writer.intramolecular_constraint_dct(
        CH3CH2_H_ZMA, (CH3CH2_ZMA, H_ZMA))
    assert ref_const_dct == const_dct  # add numpy check


def __pivot():
    """ test varecof_io.writer.build_pivot_frames
        test varecof_io.writer.calc_pivot_angles
        test varecof_io.writer.calc_pivot_xyzs
    """

    tot_geo, isol_fgeos = varecof_io.writer.fragment_geometries(
        CH3CH2_H_ZMA, (CH3CH2_ZMA, H_ZMA), FRM_KEYS)
    print(tot_geo)
    print(isol_fgeos[0])
    print(isol_fgeos[1])
    frames, npivots = varecof_io.writer.build_pivot_frames(
        tot_geo, isol_fgeos, FRM_KEYS)
    angles = varecof_io.writer.calc_pivot_angles(
        isol_fgeos, frames)
    xyzs = varecof_io.writer.calc_pivot_xyzs(
        tot_geo, isol_fgeos, FRM_KEYS)

    print(frames, npivots)
    print(angles)
    print(xyzs)


def test__face_symm():
    """ test varecof_io.writer.assess_face_symmetries(fgeo1, fgeo2)
    """

    fgeo1 = automol.zmat.geometry(CH3CH2_ZMA)
    fgeo2 = automol.zmat.geometry(H_ZMA)
    faces, face_symm = varecof_io.writer.assess_face_symmetries(fgeo1, fgeo2)

    print(faces)
    print(face_symm)

    # assert faces == ()
    # assert face_symm = 0


if __name__ == '__main__':
    test__constraint()
    __pivot()
    test__face_symm()
