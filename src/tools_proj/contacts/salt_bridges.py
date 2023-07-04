"""
Code to identify salt bridge based interactions
"""
from typing import Optional
from MDAnalysis.analysis import distances

# constants.
SB_RES_ATOMS_POSITIVE = {"LYS" : "name NZ", "ARG": "name NE NH1 NH2"}
SB_RES_ATOMS_NEGATIVE = {"ASP" : "name OD1 OD2", "GLU": "name OE1 OE2"}
SB_DIST_CUTOFF = 4 # Ångstrom

def check_for_salt_bridge(res_numbers:tuple[int, int], universe) -> Optional[str]:
    """Given two residues, test if they meet the requirements to be a salt bridge"""
    res1_numb, res2_numb = res_numbers
    res1_sc_atoms = universe.select_atoms("not name C CA O N H and resid " + str(res1_numb))
    res2_sc_atoms = universe.select_atoms("not name C CA O N H and resid " + str(res2_numb))
    res1_name, res2_name = res1_sc_atoms.resnames[0], res2_sc_atoms.resnames[0]

    if (res1_name in SB_RES_ATOMS_POSITIVE) and (res2_name in SB_RES_ATOMS_NEGATIVE):
        sb_res1_atoms = res1_sc_atoms.select_atoms(SB_RES_ATOMS_POSITIVE[res1_name])
        sb_res2_atoms = res2_sc_atoms.select_atoms(SB_RES_ATOMS_NEGATIVE[res2_name])
    elif (res1_name in SB_RES_ATOMS_NEGATIVE) and (res2_name in SB_RES_ATOMS_POSITIVE):
        sb_res1_atoms = res1_sc_atoms.select_atoms(SB_RES_ATOMS_NEGATIVE[res1_name])
        sb_res2_atoms = res2_sc_atoms.select_atoms(SB_RES_ATOMS_POSITIVE[res2_name])
    else: # salt bridge not possible
        return None

    sb_dists = distances.distance_array(
        sb_res1_atoms.positions,
        sb_res2_atoms.positions,
        box=universe.dimensions
    )

    if sb_dists.min() > SB_DIST_CUTOFF: # too far away
        return None

    # info about detected salt bridge.
    return res1_name + str(res1_numb) + " " + res2_name + str(res2_numb) + " SaltBridge " + "SC-SC"
