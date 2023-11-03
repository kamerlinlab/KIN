"""
Code to identify Van der Waals interactions.

Definitions:
mc = main chain
sc = side chain
wc = whole chain (both bc and sc used in an interaction).
"""
from typing import Optional
import numpy as np
from MDAnalysis import Universe
from MDAnalysis.analysis.distances import distance_array

# constants.
VDW_DIST_CUT = 4.5  # Ångstrom


def check_for_vdw_interaction(
    res_numbers: tuple[int, int], universe: Universe
) -> Optional[str]:
    """
    Given two residues, test if they have a salt bridge interaction.
    Function exits early when it becomes clear there is no interaction.

    Definitions:
    mc = main chain
    sc = side chain
    wc = whole chain (both mc and sc used in an interaction).

    Parameters
    ----------
    res_numbers: tuple[int, int]
        Two residues to test if there is a vdw's interaction.

    universe: Universe
        MDAnalysis universe object.

    Returns
    -------
    Optional[str]
        If interaction present then a str is returned describing the vdw's interaction.
        If no vdw's interaction, None returned.
    """
    res1_numb, res2_numb = res_numbers
    res1_name = universe.residues.resnames[res1_numb - 1]  # 0-indexed
    res2_name = universe.residues.resnames[res2_numb - 1]  # 0-indexed

    # ~3x faster to test all distances now,
    # instead of waiting until all selections are made below.
    res1_atoms = universe.select_atoms(f"not name H* and resid {str(res1_numb)}")
    res2_atoms = universe.select_atoms(f"not name H* and resid {str(res2_numb)}")

    min_dist = np.min(distance_array(res1_atoms.positions, res2_atoms.positions))

    if min_dist > VDW_DIST_CUT:
        return None

    # Build selections of the mcs and scs (where possible)
    # (OXT is an oxygen that can be found on a C-terminal residue backbone)
    res1_mc_sele_str = "name N CA C O OXT and resid " + str(res1_numb)
    res2_mc_sele_str = "name N CA C O OXT and resid " + str(res2_numb)
    vdw_res1_mc_atoms = universe.select_atoms(res1_mc_sele_str)
    vdw_res2_mc_atoms = universe.select_atoms(res2_mc_sele_str)

    if res1_name != "GLY":
        res1_sc_sele_str = "not name H* N CA C O and resid " + str(res1_numb)
        vdw_res1_sc_atoms = universe.select_atoms(res1_sc_sele_str)

    if res2_name != "GLY":
        res2_sc_sele_str = "not name H* N CA C O and resid " + str(res2_numb)
        vdw_res2_sc_atoms = universe.select_atoms(res2_sc_sele_str)

    # calculate the min distance between all available pairs.
    min_dists = {}
    min_dists["mc_mc"] = np.min(
        distance_array(vdw_res1_mc_atoms.positions, vdw_res2_mc_atoms.positions)
    )

    if res1_name != "GLY":
        min_dists["sc_mc"] = np.min(
            distance_array(vdw_res1_sc_atoms.positions, vdw_res2_mc_atoms.positions)
        )

    if res2_name != "GLY":
        min_dists["mc_sc"] = np.min(
            distance_array(vdw_res1_mc_atoms.positions, vdw_res2_sc_atoms.positions)
        )

    if (res1_name != "GLY") and (res2_name != "GLY"):
        min_dists["sc_sc"] = np.min(
            distance_array(vdw_res1_sc_atoms.positions, vdw_res2_sc_atoms.positions)
        )

    # determine which parts (mainchain or sidechain or both) are involved for both residues.
    # wc = whole chain, i.e. both mc and sc interacting for that residue.
    res1_interacting_parts, res2_interacting_parts = set(), set()
    for residue_parts, min_dist in min_dists.items():
        if min_dist > VDW_DIST_CUT:
            continue

        res1_part, res2_part = residue_parts.split("_")
        res1_interacting_parts.add(res1_part)
        res2_interacting_parts.add(res2_part)

    if len(res1_interacting_parts) > 1:
        res1_label = "wc"
    else:
        res1_label = list(res1_interacting_parts)[0]

    if len(res2_interacting_parts) > 1:
        res2_label = "wc"
    else:
        res2_label = list(res2_interacting_parts)[0]

    # info about detected vdw interaction.
    return (
        res1_name
        + str(res1_numb)
        + " "
        + res2_name
        + str(res2_numb)
        + " vdw "
        + res1_label
        + "-"
        + res2_label
    )
