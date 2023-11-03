"""
Module to handle making PyMOL compataible output files to display results.
"""
from typing import Any, Optional
from pathlib import Path


def project_pymol_res_res_scores(
    res_res_scores: dict[tuple[int, int], float],
    out_file: str,
    res_res_colors: Optional[dict[tuple[int, int], bool]] = None,
) -> None:
    """
    Write out a PyMOL compatible python script to project residue-residue scores.
    The scores will be depicted as as cylinders between each interacting residue pair.
    Cylinder size will be controlled according to the relative score.

    Returns nothing as file saved to disk.

    Parameters
    ----------
    res_res_scores : dict[tuple[int, int], float]
        Keys are the residue pair and each value is their associated scores.
        Key formatting is a tuple of 2 integers, residue number 1 and residue number 2.

    out_file: str
        Save the file to this path.

    res_res_colors: Optional[ dict[tuple[int, int], str] ]
        Keys are the residue pair and each value is the assigned color.
        Defines color to draw each interaction.
        Optional parameter, all interactions will be colored red otherwise.
    """
    # first, rescale the scores/results so the drawn cylinder radii looks good.
    rescaled_scores = _rescale_scores(input_dict=res_res_scores, new_max_value=0.3)

    # Header of output file.
    out_contents = "# To use this script you can:\n"
    out_contents += "# 1. Load the PDB file of your system in PyMOL.\n"
    out_contents += "# 2. Run this file with:'@[FILE_NAME]' in the command line.\n"
    out_contents += "# 3. Make sure this file is in the same directory as the pdb.\n"

    # main section.
    numb = 1
    for interaction_pair, radius in rescaled_scores.items():
        res1, res2 = interaction_pair

        if res_res_colors is not None:
            color = res_res_colors[(res1, res2)]
        else:
            color = "red"

        feature_rep = (
            f"distance interaction{numb}, "
            + f"resid {str(res1)} and name CA, "
            + f"resid {str(res2)} and name CA \n"
            + f"set dash_radius, {radius}, interaction{numb} \n"
            f"set dash_color, {color}, interaction{numb} \n"
        )
        out_contents += feature_rep

        numb += 1
    # Finally, group all draw interactions made together,
    # (easier for a user to handle in PyMOL)
    out_contents += "group All_Interactions, interaction* \n"
    out_contents += "set dash_gap, 0.00, All_Interactions \n"
    out_contents += "set dash_round_ends, on, All_Interactions \n"
    out_contents += "hide labels \n"

    # finished
    _save_pymol_file(out_file=out_file, contents=out_contents)


def project_pymol_per_res_scores(
    per_res_scores: dict[int, float],
    out_file: str,
) -> None:
    """
    Write out a PyMOL compatible script that projects per residue scores.
    This script will show the Calpha carbon of every residue as a sphere,
    and then scale the size of the sphere according to its relative score.

    Parameters
    ----------
    per_res_scores: dict
        The keys are each residue and values the per residue score.

    out_file: str
        Save the file to this path.
    """
    # first, rescale the scores/results so the spheres looks good.
    rescaled_scores = _rescale_scores(input_dict=per_res_scores, new_max_value=1.0)

    # Header of output file.
    out_contents = "# To use this script you can:\n"
    out_contents += "# 1. Load the PDB file of your system in PyMOL.\n"
    out_contents += "# 2. Run this file with:'@[FILE_NAME]' in the command line.\n"
    out_contents += "# 3. Make sure this file is in the same directory as the pdb.\n"

    # Main, tells PyMOL to show spheres and set their size accordingly.
    for res_numb, sphere_size in rescaled_scores.items():
        out_contents += f"show spheres, resi {res_numb} and name CA\n"
        out_contents += (
            f"set sphere_scale, {sphere_size:.4f}, resi {res_numb} and name CA\n"
        )

    # user selection of all CA carbons so easy to modify the sphere colours etc...
    all_spheres_list = list(per_res_scores.keys())
    all_spheres_str = "+".join(map(str, all_spheres_list))
    out_contents += f"sele All_Spheres, resi {all_spheres_str} and name CA\n"

    # finished
    _save_pymol_file(out_file=out_file, contents=out_contents)


def gen_per_res_scores(
    res_res_scores: dict[tuple[int, int], float]
) -> dict[int, float]:
    """
    Convert a set of residue-residue scores to per residue scores.
    For each residue, the scores of each interaction in which it is involved in are summed.
    Then these results are normalised, so that the largest residue has value 1.

    Parameters
    ----------
    res_res_scores : dict[tuple[int, int], float]
        Keys are the residue pair and each value is their associated scores.
        Key formatting is a tuple of 2 integers, residue number 1 and residue number 2.

    Returns
    ----------
    per_res_scores: dict
        The keys are each residue and values the per residue score.
    """
    # determine max_residue number
    biggest_res = 1
    for keys in res_res_scores:
        if keys[0] > biggest_res:
            biggest_res = keys[0]
        if keys[1] > biggest_res:
            biggest_res = keys[1]

    # generate a set of per residue scores to populate.
    per_res_scores = {}
    for res_numb in range(1, biggest_res + 1):
        per_res_scores[res_numb] = 0

    for res_res_pair, score in res_res_scores.items():
        res1, res2 = res_res_pair
        per_res_scores[res1] += score
        per_res_scores[res2] += score

    scaled_per_res_scores = _rescale_scores(
        input_dict=per_res_scores, new_max_value=1.0
    )
    return scaled_per_res_scores


def _save_pymol_file(out_file: str, contents: str) -> None:
    """
    Save a PyMOL output file.

    Parameters
    ----------
    out_file:str
        File path to write the file to.

    contents: str
        The contents of the file to write.
    """
    out_file_safe = Path(out_file)
    with open(out_file_safe, "w+", encoding="utf-8") as file_out:
        file_out.write(contents)
    print(f"The file: {out_file_safe} was written to disk.")


def _rescale_scores(
    input_dict: dict[Any, float], new_max_value: float
) -> dict[Any, float]:
    """
    Rescale a dictionary containing per residue or residue-residue scores/counts etc..

    Parameters
    ----------
    input_dict : dict[Any, float]
        Keys can be any format, they will be returned as is.

    max_value : float
        Rescale the values so that this is the max value in the returned dictionary.

    Returns
    ----------
    dict[Any, float]
        Rescaled scores, keys will be untouched.
    """
    max_strength = max(list(input_dict.values()))
    scale_factor = max_strength / new_max_value

    rescaled_dict = {}
    for key, curr_value in input_dict.items():
        new_value = round((curr_value / scale_factor), 4)
        rescaled_dict.update({key: new_value})

    return rescaled_dict
