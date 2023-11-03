"""
Code to identify cation-pi interactions

Definitions are sourced from: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8338773/
"""
from typing import Optional
import numpy as np
from MDAnalysis import Universe
from MDAnalysis.analysis import distances

from kin.contacts.utils import angle_between_two_vectors, normal_vector_3_atoms

# Constants
CAT_PI_RES_ATOMS_CATION = {"LYS": "NZ", "ARG": "CZ"}
CAT_PI_RES_ATOMS_CATION_COM = "NH1 NH2 NE"  # only for ARG
CAT_PI_RES_ATOMS_PI = {
    "TRP": "CE2 CE3 CH2",
    "TYR": "CG CE1 CE2",
    "PHE": "CG CE1 CE2",
    "HIE": "CG CD2 CE1",
    "HID": "CG CD2 CE1",
}  # HIP not included as positive

# cutoffs
CATION_PI_D_CUT = 6
CATION_PI_ANGLE_TOLERANCE = 30  # how close to ideal the angle needs to be.

# Ideal values
CATION_PI_THETA_1_IDEAL = 0  # Applies to ARG and LYS, Either stacked and T-shaped
CATION_PI_THETA_2_STACKED_IDEAL = 0  # Only applies to ARG
CATION_PI_THETA_2_TSHAPED_IDEAL = 90  # Only applies to ARG


def check_for_cation_pi(
    res_numbers: tuple[int, int], universe: Universe
) -> Optional[str]:
    """
    Given two residues, test if they have a cation-pi interaction.
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
        If cation-pi present then a str is returned describing the cation-pi.
        If no cation-pi, None returned.
    """
    res1_numb, res2_numb = res_numbers
    res1_name = universe.residues.resnames[res1_numb - 1]  # 0-indexed
    res2_name = universe.residues.resnames[res2_numb - 1]  # 0-indexed

    if (res1_name in CAT_PI_RES_ATOMS_CATION) and (res2_name in CAT_PI_RES_ATOMS_PI):
        res1_sele_str = (
            "name "
            + CAT_PI_RES_ATOMS_CATION[res1_name]
            + " and resid "
            + str(res1_numb)
        )
        res2_sele_str = (
            "name " + CAT_PI_RES_ATOMS_PI[res2_name] + " and resid " + str(res2_numb)
        )
        cp_cation_atom = universe.select_atoms(res1_sele_str)
        cp_pi_atoms = universe.select_atoms(res2_sele_str)

        if res1_name == "ARG":
            arg_sele_str = (
                "name " + CAT_PI_RES_ATOMS_CATION_COM + " and resid " + str(res1_numb)
            )
            cp_cation_atom_com = universe.select_atoms(arg_sele_str)

    elif (res1_name in CAT_PI_RES_ATOMS_PI) and (res2_name in CAT_PI_RES_ATOMS_CATION):
        res1_sele_str = (
            "name " + CAT_PI_RES_ATOMS_PI[res1_name] + " and resid " + str(res1_numb)
        )
        res2_sele_str = (
            "name "
            + CAT_PI_RES_ATOMS_CATION[res2_name]
            + " and resid "
            + str(res2_numb)
        )
        cp_pi_atoms = universe.select_atoms(res1_sele_str)
        cp_cation_atom = universe.select_atoms(res2_sele_str)

        if res2_name == "ARG":
            arg_sele_str = (
                "name " + CAT_PI_RES_ATOMS_CATION_COM + " and resid " + str(res2_numb)
            )
            cp_cation_atom_com = universe.select_atoms(arg_sele_str)

    else:
        return None

    # distance check.
    cp_dist = distances.distance_array(
        cp_pi_atoms.center_of_mass(), cp_cation_atom.positions, box=universe.dimensions
    )
    if cp_dist > CATION_PI_D_CUT:  # bad distance
        return None

    # Theta 1 calculation.
    arom_normal_vector = normal_vector_3_atoms(cp_pi_atoms.positions)
    arom_cation_vector = (cp_pi_atoms.center_of_mass() - cp_cation_atom.positions)[0]
    cp_theta_1 = angle_between_two_vectors(arom_normal_vector, arom_cation_vector)

    delta_theta_1 = min(
        np.abs(cp_theta_1 - CATION_PI_THETA_1_IDEAL),
        np.abs(cp_theta_1 - CATION_PI_THETA_1_IDEAL - 180),
    )

    if delta_theta_1 > CATION_PI_ANGLE_TOLERANCE:
        return None  # bad angle

    if (res1_name == "LYS") or (
        res2_name == "LYS"
    ):  # Requirements passed for cation-pi
        return (
            res1_name
            + str(res1_numb)
            + " "
            + res2_name
            + str(res2_numb)
            + " cationpi "
            + "sc-sc"
        )

    # Means it is "Arg", so need to test theta2
    cation_normal_vector = normal_vector_3_atoms(cp_cation_atom_com.positions)
    cp_theta_2 = angle_between_two_vectors(cation_normal_vector, arom_normal_vector)

    delta_stacked_ideal = min(
        np.abs(cp_theta_2 - CATION_PI_THETA_2_STACKED_IDEAL),
        np.abs(cp_theta_2 - CATION_PI_THETA_2_STACKED_IDEAL - 180),
    )
    if delta_stacked_ideal <= CATION_PI_ANGLE_TOLERANCE:
        # Stacked Arg
        return (
            res1_name
            + str(res1_numb)
            + " "
            + res2_name
            + str(res2_numb)
            + " cationpi "
            + "sc-sc"
        )

    delta_tshaped_ideal = min(
        np.abs(cp_theta_2 - CATION_PI_THETA_2_TSHAPED_IDEAL),
        np.abs(cp_theta_2 - CATION_PI_THETA_2_TSHAPED_IDEAL - 180),
    )
    if delta_tshaped_ideal <= CATION_PI_ANGLE_TOLERANCE:
        # tshaped Arg
        return (
            res1_name
            + str(res1_numb)
            + " "
            + res2_name
            + str(res2_numb)
            + " cationpi "
            + "sc-sc"
        )

    return None  # bad theta2.
