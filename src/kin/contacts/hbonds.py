"""
Code to identify hydrogen bond interactions.
"""
from typing import Optional, Tuple
import itertools
import numpy as np
from MDAnalysis import Universe
from MDAnalysis.analysis import distances
from kin.contacts.utils import angle_between_two_vectors


SC_HBOND_RES_ATOMS_ACCEPTOR = {
    "ASN": ["OD1"],
    "ASP": ["OD1", "OD2"],
    "ASH": ["OD1", "OD2"],
    "GLN": ["OE1"],
    "GLU": ["OE1", "OE2"],
    "GLH": ["OE1", "OE2"],
    "HIE": ["ND1"],
    "HID": ["NE2"],
    "SER": ["OG"],
    "THR": ["OG1"],
    "TYR": ["OH"],
}

# keys are the donor atom, values is a list of hydrogens beloging to that donor.
SC_HBOND_RES_ATOMS_DONOR = {
    "ASN": [{"ND2": ["HD21", "HD22"]}],
    "ARG": [{"NE": ["HE"]}, {"NH1": ["HH11", "HH12"]}, {"NH2": ["HH21", "HH22"]}],
    "GLN": [{"NE2": ["HE21", "HE22"]}],
    "SER": [{"OG": ["HG"]}],
    "THR": [{"OG1": ["HG1"]}],
    "TYR": [{"OH": ["HH"]}],
    "HIE": [{"NE2": ["HE2"]}],
    "HID": [{"ND1": ["HD1"]}],
    "HIP": [{"NE2": ["HE2"]}, {"ND1": ["HD1"]}],
    "LYS": [{"NZ": ["HZ1", "HZ2", "HZ3"]}],
    "LYN": [{"NZ": ["HZ2", "HZ3"]}],
}

# Constants and cutoffs.
HB_DIST_CUTOFF = 3.5  # Donor-acceptor distance
HB_ANGLE_IDEAL = 180  # donor-hydrogen-acceptor
HB_ANGLE_TOLERANCE = 45  # can be +- this much from ideal.


def check_for_hbond(res_numbers: tuple[int, int], universe: Universe) -> Optional[list[str]]:
    """
    Given two residues, test if they have a hbond interaction.
    Function exits early when it becomes clear there is no interaction.

    Parameters
    ----------
    res_numbers: tuple[int, int]
        Two residues to test if there is a salt bridge.

    universe: Universe
        MDAnalysis universe object.

    Returns
    -------
    Optional[list[str]]
        If 1 or more hydrogen bond present then a list of strings is returned.
        Each str in the list describes a hydrogen bond.
        If no hydrogen bond, None returned.
    """
    res1_numb, res2_numb = res_numbers
    res1_name = universe.residues.resnames[res1_numb - 1]  # 0-indexed
    res2_name = universe.residues.resnames[res2_numb - 1]  # 0-indexed

    res1_don_res2_acc, res2_don_res1_acc = _prep_donor_acceptors(res1_name, res2_name)

    hbonds_found = []
    hbonds_found += _identify_hbond(
        donor_acceptor_combos=res1_don_res2_acc,
        donor_res_numb=res1_numb,
        acceptor_res_numb=res2_numb,
        universe=universe,
    )

    hbonds_found += _identify_hbond(
        donor_acceptor_combos=res2_don_res1_acc,
        donor_res_numb=res2_numb,
        acceptor_res_numb=res1_numb,
        universe=universe,
    )

    if len(hbonds_found) == 0:
        return None  # none found

    # figure out formatting.
    # determine which parts (mainchain or sidechain or both) are involved for both residues.
    # wc = whole chain, i.e. both mc and sc interacting for that residue.
    hbonds_formatted = []
    for hbond in hbonds_found:
        donor_res_numb, donor, acceptor_res_numb, acceptor = hbond

        if donor == "N":
            donor_part = "mc"
        else:
            donor_part = "sc"

        if acceptor in ["O", "OXT"]:
            acceptor_part = "mc"
        else:
            acceptor_part = "sc"

        if donor_res_numb < acceptor_res_numb:
            hbond_str = (
                res1_name
                + str(res1_numb)
                + " "
                + res2_name
                + str(res2_numb)
                + " hbond "
                + donor_part
                + "-"
                + acceptor_part
            )
        else:
            hbond_str = (
                res1_name
                + str(res1_numb)
                + " "
                + res2_name
                + str(res2_numb)
                + " hbond "
                + acceptor_part
                + "-"
                + donor_part
            )

        hbonds_formatted.append(hbond_str)
    return set(hbonds_formatted)


def _prep_donor_acceptors(res1_name: str, res2_name: str) -> Tuple[list, list]:
    """
    Helper function to prepare the donor and acceptors pairs to compare.
    """
    # start with the main chain donor and acceptors
    res1_acceptors, res2_acceptors = ["O", "OXT"], ["O", "OXT"]
    res1_donors, res2_donors = [{"N": ["H"]}], [{"N": ["H"]}]

    # add in side chain donor and acceptors.
    if res1_name in SC_HBOND_RES_ATOMS_ACCEPTOR:
        res1_acceptors += SC_HBOND_RES_ATOMS_ACCEPTOR[res1_name]

    if res1_name in SC_HBOND_RES_ATOMS_DONOR:
        res1_donors += SC_HBOND_RES_ATOMS_DONOR[res1_name]

    if res2_name in SC_HBOND_RES_ATOMS_ACCEPTOR:
        res2_acceptors += SC_HBOND_RES_ATOMS_ACCEPTOR[res2_name]

    if res2_name in SC_HBOND_RES_ATOMS_DONOR:
        res2_donors += SC_HBOND_RES_ATOMS_DONOR[res2_name]

    # make all possible combinations.
    res1_don_res2_acc = list(itertools.product(res1_donors, res2_acceptors))
    res2_don_res1_acc = list(itertools.product(res2_donors, res1_acceptors))
    return res1_don_res2_acc, res2_don_res1_acc


def _identify_hbond(donor_acceptor_combos, donor_res_numb, acceptor_res_numb, universe: Universe):
    """
    Given a combination of donor and acceptor atoms, test if any hydrogen bonds
    are present.
    """
    hbonds_found = []
    for donor_combo, acceptor in donor_acceptor_combos:
        donor = list(donor_combo.keys())[0]
        donor_str = "name " + donor + " and resid " + str(donor_res_numb)
        donor_atom = universe.select_atoms(donor_str)

        acceptor_str = "name " + acceptor + " and resid " + str(acceptor_res_numb)
        acceptor_atom = universe.select_atoms(acceptor_str)

        # can occur if atom names don't exist for that residue (e.g. OXT).
        if (len(donor_atom) == 0) or (len(acceptor_atom) == 0):
            continue

        # remove donor_acceptor that fail distance test.
        d_a_dist = distances.distance_array(acceptor_atom.positions, donor_atom.positions)
        if d_a_dist > HB_DIST_CUTOFF:
            continue

        for hydrogen in list(donor_combo.values())[0]:
            hydrogen_str = "name " + hydrogen + " and resid " + str(donor_res_numb)
            hydrogen_atom = universe.select_atoms(hydrogen_str)
            try:
                dh_vector = donor_atom.positions[0] - hydrogen_atom.positions[0]
            except IndexError:  # can occur for proline, as has no backbone H on nitrogen.
                continue
            ha_vector = acceptor_atom.positions[0] - hydrogen_atom.positions[0]
            dha_angle = angle_between_two_vectors(dh_vector, ha_vector)

            delta_dha_ideal = min(
                np.abs(dha_angle - HB_ANGLE_IDEAL), np.abs(dha_angle - HB_ANGLE_IDEAL - 180)
            )
            if delta_dha_ideal < HB_ANGLE_TOLERANCE:
                hbonds_found.append((donor_res_numb, donor, acceptor_res_numb, acceptor))
    return hbonds_found
