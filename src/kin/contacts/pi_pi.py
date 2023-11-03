"""
Code to identify pi-pi interactions.

Describe types included here.

Definitions are sourced from: https://link.springer.com/article/10.1007/s12539-015-0263-z
"""
from typing import Optional
import numpy as np
from MDAnalysis import Universe
from MDAnalysis.analysis import distances

from kin.contacts.utils import angle_between_two_vectors, normal_vector_3_atoms

# Constants
# From souce, 5 membered rings used for pi-pi stacking for TRP.
PI_PI_RES_ATOMS = {
    "TYR": "CG CE1 CE2",
    "PHE": "CG CE1 CE2",
    "TRP": "CG CD2 NE1",
    "HIE": "CG CD2 CE1",
    "HID": "CG CD2 CE1",
}  # HIP not included as positive

# Cutoffs
PI_PI_D_CUT = 7.2
# Defintions based on ranges.
PI_PI_GAMMA_STACK_RANGE = (-30, 30)  # also called parralel.
PI_PI_GAMMA_TSHAPED_RANGE = (50, 130)
# Other values would be classified as "intermediate".


def check_for_pi_pi(
    res_numbers: tuple[int, int], universe: Universe, detailed_information: bool = False
) -> Optional[str]:
    """
    Given two residues, test if they have a pi-pi interaction.
    Function exits early when it becomes clear there is no interaction.

    Parameters
    ----------
    res_numbers: tuple[int, int]
        Two residues to test if there is a salt bridge.

    universe: Universe
        MDAnalysis universe object.

    detailed_information: bool
        If detailed information about the type of pi-pi stacking interaction should be returned.
        Default is: False

    Returns
    -------
    Optional[str]
        If pi-pi present then a str is returned describing the pi-pi.
        If no pi-pi, None returned.
    """
    res1_numb, res2_numb = res_numbers
    res1_name = universe.residues.resnames[res1_numb - 1]  # 0-indexed
    res2_name = universe.residues.resnames[res2_numb - 1]  # 0-indexed

    if (res1_name not in PI_PI_RES_ATOMS) or (res2_name not in PI_PI_RES_ATOMS):
        return None  # not possible.

    # extract atoms needed for testing.
    res1_sele_str = (
        "name " + PI_PI_RES_ATOMS[res1_name] + " and resid " + str(res1_numb)
    )
    res2_sele_str = (
        "name " + PI_PI_RES_ATOMS[res2_name] + " and resid " + str(res2_numb)
    )
    res1_pi_atoms = universe.select_atoms(res1_sele_str)
    res2_pi_atoms = universe.select_atoms(res2_sele_str)

    # distance check.
    com_dist = distances.distance_array(
        res1_pi_atoms.center_of_mass(),
        res2_pi_atoms.center_of_mass(),
        box=universe.dimensions,
    )
    if com_dist > PI_PI_D_CUT:
        return None  # too far away

    # Determine the angles required to classify the pi-pi stacking type.
    res1_normal_vector = normal_vector_3_atoms(res1_pi_atoms.positions)
    res2_normal_vector = normal_vector_3_atoms(res2_pi_atoms.positions)
    pi_pi_vector = res1_pi_atoms.center_of_mass() - res2_pi_atoms.center_of_mass()

    theta = angle_between_two_vectors(res1_normal_vector, pi_pi_vector) - 90
    delta = angle_between_two_vectors(res2_normal_vector, pi_pi_vector) - 90
    # correct for periodicity.
    theta_corrected = min(np.abs(theta), np.abs(theta - 180))
    delta_corrected = min(np.abs(delta), np.abs(delta - 180))

    if (theta_corrected <= 30) and (delta_corrected <= 30):
        return None  # if theta and delta are both close to 0, no pi overlap.

    # Enough information to say this is a pi-pi stacking interaction now.
    if not detailed_information:
        return (
            res1_name
            + str(res1_numb)
            + " "
            + res2_name
            + str(res2_numb)
            + " pipi "
            + "sc-sc"
        )

    # Determine the specific type of pi-pi interaction.
    gamma = angle_between_two_vectors(res1_normal_vector, res2_normal_vector)
    gamma_corrected = min(np.abs(gamma), np.abs(gamma - 180))

    if PI_PI_GAMMA_TSHAPED_RANGE[0] <= gamma_corrected <= PI_PI_GAMMA_TSHAPED_RANGE[1]:
        return (
            res1_name
            + str(res1_numb)
            + " "
            + res2_name
            + str(res2_numb)
            + " pipi_t_shaped "
            + "sc-sc"
        )

    if (gamma_corrected >= PI_PI_GAMMA_STACK_RANGE[0]) and (
        gamma_corrected <= PI_PI_GAMMA_STACK_RANGE[1]
    ):
        # Then stacked/parralel.

        if (theta_corrected >= 80) or (delta_corrected >= 80):
            return (
                res1_name
                + str(res1_numb)
                + " "
                + res2_name
                + str(res2_numb)
                + " pipi_stacked_face_to_face  "
                + "sc-sc"
            )

        # otherwise offset stacked
        return (
            res1_name
            + str(res1_numb)
            + " "
            + res2_name
            + str(res2_numb)
            + " pipi_stacked_offset "
            + "sc-sc"
        )

    # if not either of the above, then "intermediate conformation"
    return (
        res1_name
        + str(res1_numb)
        + " "
        + res2_name
        + str(res2_numb)
        + " pipi_intermediate_conf "
        + "sc-sc"
    )
