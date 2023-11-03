"""
Code to identify salt bridge based interactions
"""
from typing import Optional
from MDAnalysis import Universe
from MDAnalysis.analysis import distances

# constants.
SB_RES_ATOMS_POSITIVE = {"LYS": "NZ", "ARG": "NE NH1 NH2"}
SB_RES_ATOMS_NEGATIVE = {"ASP": "OD1 OD2", "GLU": "OE1 OE2"}
SB_DIST_CUTOFF = 4.5  # Ångstrom


def check_for_salt_bridge(res_numbers: tuple[int, int], universe: Universe) -> Optional[str]:
    """
    Given two residues, test if they have a salt bridge interaction.
    Function exits early when it becomes clear there is no interaction.

    Parameters
    ----------
    res_numbers: tuple[int, int]
        Two residues to test if there is a salt bridge.

    universe: Universe
        MDAnalysis universe object.

    Returns
    -------
    Optional[str]
        If salt bridge present then a str is returned describing the salt bridge.
        If no salt bridge, None returned.
    """
    res1_numb, res2_numb = res_numbers
    res1_name = universe.residues.resnames[res1_numb - 1]  # 0-indexed
    res2_name = universe.residues.resnames[res2_numb - 1]  # 0-indexed

    if (res1_name in SB_RES_ATOMS_POSITIVE) and (res2_name in SB_RES_ATOMS_NEGATIVE):
        res1_sele_str = "name " + SB_RES_ATOMS_POSITIVE[res1_name] + " and resid " + str(res1_numb)
        res2_sele_str = "name " + SB_RES_ATOMS_NEGATIVE[res2_name] + " and resid " + str(res2_numb)
        sb_res1_atoms = universe.select_atoms(res1_sele_str)
        sb_res2_atoms = universe.select_atoms(res2_sele_str)

    elif (res1_name in SB_RES_ATOMS_NEGATIVE) and (res2_name in SB_RES_ATOMS_POSITIVE):
        res1_sele_str = "name " + SB_RES_ATOMS_NEGATIVE[res1_name] + " and resid " + str(res1_numb)
        res2_sele_str = "name " + SB_RES_ATOMS_POSITIVE[res2_name] + " and resid " + str(res2_numb)
        sb_res1_atoms = universe.select_atoms(res1_sele_str)
        sb_res2_atoms = universe.select_atoms(res2_sele_str)

    else:  # salt bridge not possible
        return None

    sb_dists = distances.distance_array(
        sb_res1_atoms.positions, sb_res2_atoms.positions, box=universe.dimensions
    )

    if sb_dists.min() > SB_DIST_CUTOFF:  # too far away
        return None

    # info about detected salt bridge.
    return res1_name + str(res1_numb) + " " + res2_name + str(res2_numb) + " saltbridge " + "sc-sc"


def check_for_c_term_salt_bridge(
    res_numbers: tuple[int, int],
    c_term_res_numbs: list[int],
    universe: Universe,
) -> Optional[str]:
    """
    Test if a c-terminal residue is forming a salt bridge using its main chain atoms (O and OXT).
    This function only deals with this special "edge case".
    Function exits early when it becomes clear there is no interaction.

    Parameters
    ----------
    res_numbers: tuple[int, int]
        Two residues to test if there is a salt bridge.

    c_term_res_numbs: list[int],
        List of all residue numbers that are c-terminal residues.
        (i.e., they have a negatively charged backbone).

    universe: Universe
        MDAnalysis universe object.

    Returns
    -------
    Optional[str]
        If salt bridge present then a str is returned describing the salt bridge.
        If no salt bridge, None returned.
    """
    res1_numb, res2_numb = res_numbers
    res1_name = universe.residues.resnames[res1_numb - 1]  # 0-indexed
    res2_name = universe.residues.resnames[res2_numb - 1]  # 0-indexed

    if (res1_numb in c_term_res_numbs) and (res2_name in SB_RES_ATOMS_POSITIVE):
        c_term_res_sele_str = "name O OXT and resid " + str(res1_numb)
        pos_res_sele_str = "name " + SB_RES_ATOMS_POSITIVE[res2_name] + " and resid " + str(res2_numb)

    elif (res1_name in SB_RES_ATOMS_POSITIVE) and (res2_numb in c_term_res_numbs):
        pos_res_sele_str = "name " + SB_RES_ATOMS_POSITIVE[res1_name] + " and resid " + str(res1_numb)
        c_term_res_sele_str = "name O OXT and resid " + str(res2_numb)
    else:  # not possible
        return None

    pos_res_atoms = universe.select_atoms(pos_res_sele_str)
    c_term_res_atoms = universe.select_atoms(c_term_res_sele_str)

    sb_dists = distances.distance_array(
        pos_res_atoms.positions, c_term_res_atoms.positions, box=universe.dimensions
    )
    if sb_dists.min() > SB_DIST_CUTOFF:  # too far away
        return None

    # return info about detected salt bridge.
    # Diff return strings, define which residue is interacting from side/main chain.
    if res1_numb in c_term_res_numbs:
        return res1_name + str(res1_numb) + " " + res2_name + str(res2_numb) + " saltbridge mc-sc"

    return res1_name + str(res1_numb) + " " + res2_name + str(res2_numb) + " saltbridge sc-mc"
