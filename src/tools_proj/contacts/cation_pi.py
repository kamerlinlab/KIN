"""
Code to identify cation-py interactions

Definitions are sourced from: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8338773/
"""
from typing import Optional
import numpy as np
from MDAnalysis.analysis import distances

from tools_proj.contacts.utils import angle_between_two_vectors, normal_vector_3_atoms

# Constants
CAT_PI_RES_ATOMS_CATION = {"LYS": "name NZ", "ARG": "name CZ"}
CAT_PI_RES_ATOMS_CATION_COM = "name NH1 NH2 NE" # only for ARG
CAT_PI_RES_ATOMS_PI = {"TRP": "name CE2 CE3 CH2", "TYR": "name CG CE1 CE2",
                       "PHE": "name CG CE1 CE2", "HIE": "name CG CD2 CE1",
                       "HID": "name CG CD2 CE1"} # HIP not included as positive

# cutoffs
CATION_PI_D_CUT = 6
CATION_PI_ANGLE_TOLERANCE = 30 # how close to ideal the angle needs to be.

# Ideal values
CATION_PI_THETA_1_IDEAL = 0 # Applies to ARG and LYS, Either stacked and T-shaped
CATION_PI_THETA_2_STACKED_IDEAL = 0 # Only applies to ARG
CATION_PI_THETA_2_TSHAPED_IDEAL = 90 # Only applies to ARG


def check_for_cation_pi(res_numbers:tuple[int, int], universe) -> Optional[str]:
    """Given two residues, test if they have a cation-pi interaction"""
    res1_numb, res2_numb = res_numbers
    res1_sc_atoms = universe.select_atoms("not name C CA O N H and resid " + str(res1_numb))
    res2_sc_atoms = universe.select_atoms("not name C CA O N H and resid " + str(res2_numb))
    res1_name, res2_name = res1_sc_atoms.resnames[0], res2_sc_atoms.resnames[0]


    if (res1_name in CAT_PI_RES_ATOMS_CATION) and (res2_name in CAT_PI_RES_ATOMS_PI):
        cp_cation_atom = res1_sc_atoms.select_atoms(CAT_PI_RES_ATOMS_CATION[res1_name])
        cp_pi_atoms = res2_sc_atoms.select_atoms(CAT_PI_RES_ATOMS_PI[res2_name])

        if res1_name == "ARG":
            cp_cation_atom_com = res1_sc_atoms.select_atoms(CAT_PI_RES_ATOMS_CATION_COM)

    elif (res1_name in CAT_PI_RES_ATOMS_PI) and (res2_name in CAT_PI_RES_ATOMS_CATION):
        cp_pi_atoms = res1_sc_atoms.select_atoms(CAT_PI_RES_ATOMS_PI[res1_name])
        cp_cation_atom = res2_sc_atoms.select_atoms(CAT_PI_RES_ATOMS_CATION[res2_name])

        if res2_name == "ARG":
            cp_cation_atom_com = res2_sc_atoms.select_atoms(CAT_PI_RES_ATOMS_CATION_COM)

    else:
        return None

    # distance check.
    cp_dist = distances.distance_array(cp_pi_atoms.center_of_mass(), cp_cation_atom.positions, box=universe.dimensions)
    if cp_dist > CATION_PI_D_CUT: # too far away
        return None

    # Theta 1 calculation.
    arom_normal_vector = normal_vector_3_atoms(cp_pi_atoms.positions)
    arom_cation_vector = (cp_pi_atoms.center_of_mass() - cp_cation_atom.positions)[0]
    cp_theta_1 = angle_between_two_vectors(arom_normal_vector, arom_cation_vector)

    delta_theta_1 = min(
        np.abs(cp_theta_1 - CATION_PI_THETA_1_IDEAL),
        np.abs(cp_theta_1 - CATION_PI_THETA_1_IDEAL - 180)
    )

    if delta_theta_1 > CATION_PI_ANGLE_TOLERANCE:
        return None # bad angle

    if (res1_name == "LYS") or (res2_name == "LYS"): # Requirements passed for cation-pi
        return res1_name + str(res1_numb) + " " + res2_name + str(res2_numb) + " CationPi " + "SC-SC"

    # if "Arg", then need to test theta2
    cation_normal_vector = normal_vector_3_atoms(cp_cation_atom_com.positions)
    cp_theta_2 = angle_between_two_vectors(cation_normal_vector, arom_normal_vector)

    delta_stacked_ideal = min(
        np.abs(cp_theta_2 - CATION_PI_THETA_2_STACKED_IDEAL),
        np.abs(cp_theta_2 - CATION_PI_THETA_2_STACKED_IDEAL - 180)
    )
    if delta_stacked_ideal <= CATION_PI_ANGLE_TOLERANCE:
        # Stacked Arg
        return res1_name + str(res1_numb) + " " + res2_name + str(res2_numb) + " CationPi " + "SC-SC"

    delta_tshaped_ideal = min(
        np.abs(cp_theta_2 - CATION_PI_THETA_2_TSHAPED_IDEAL),
        np.abs(cp_theta_2 - CATION_PI_THETA_2_TSHAPED_IDEAL - 180)
    )
    if delta_tshaped_ideal <= CATION_PI_ANGLE_TOLERANCE:
        # tshaped Arg
        return res1_name + str(res1_numb) + " " + res2_name + str(res2_numb) + " CationPi " + "SC-SC"


    return None # bad theta2.
