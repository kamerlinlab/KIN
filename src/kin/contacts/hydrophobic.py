"""
Code to identify hydrophobic interactions.
"""
from typing import Optional
from MDAnalysis import Universe
from MDAnalysis.analysis import distances

# constants.
HYDROPHOBIC_RES = (
    "ALA",
    "VAL",
    "LEU",
    "ILE",
    "PRO",
    "TRP",
    "PHE",
    "CYS",  # Regular cystine
    "CYX",  # Disulfide bridged cystine
    "MET",
)
HYDROPHOBIC_CUTOFF_DIST = 4  # Ångstrom


def check_for_hydrophobic(
    res_numbers: tuple[int, int], universe: Universe
) -> Optional[str]:
    """Function identify hydrophobic interactions between two provided residues."""
    res1_numb, res2_numb = res_numbers
    res1_name = universe.residues.resnames[res1_numb - 1]  # 0-indexed
    res2_name = universe.residues.resnames[res2_numb - 1]  # 0-indexed

    if (res1_name not in HYDROPHOBIC_RES) or (res2_name not in HYDROPHOBIC_RES):
        return None  # not possible.

    if (res1_name == "CYX") and (res2_name == "CYX"):
        return None  # would be a disulfide bridge

    # catches all side chain carbon atoms
    res1_sc_sele = "name C* and not name CA C and resid " + str(res1_numb)
    res1_sc_atoms = universe.select_atoms(res1_sc_sele)
    res2_sc_sele = "name C* and not name CA C and resid " + str(res2_numb)
    res2_sc_atoms = universe.select_atoms(res2_sc_sele)

    dist = distances.distance_array(
        res1_sc_atoms.positions, res2_sc_atoms.positions, box=universe.dimensions
    )

    if dist.min() > HYDROPHOBIC_CUTOFF_DIST:
        return None

    return (
        res1_name
        + str(res1_numb)
        + " "
        + res2_name
        + str(res2_numb)
        + " hydrophobic "
        + "sc-sc"
    )
