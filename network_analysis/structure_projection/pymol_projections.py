"""
Set of functions to make pymol projections of the contacts data results.

"""
from pathlib import Path


def project_pymol_res_res_scores(
    res_res_scores: dict[tuple[int, int], float],
    out_file: str,
) -> None:
    """
    Write out a PyMOL compatible python script to project residue-residue scores.
    The scores will be depicted as as cylinders between each interacting residue pair.
    Cylinder size will be controlled accordning to the relative score and colour by
    the interaction type.

    Parameters
    ----------
    res_res_scores : dict[tuple[int, int], float]
        Keys are the residue pair and each value is their associated scores.
        Key formatting is a tuple of 2 integers, residue number 1 and residue number 2.

    out_file: str
        Save the file to this path.
    """

    # Header of output file.
    out_file_contents = ""
    out_file_contents += (
        "# You can run me in several ways, perhaps the easiest way is to:\n"
    )
    out_file_contents += "# 1. Load the PDB file of your system in PyMOL.\n"
    out_file_contents += "# 2. Download and run the draw_links.py script.\n"
    out_file_contents += "# It can be obtained from: "
    out_file_contents += (
        "# http://pldserver1.biochem.queensu.ca/~rlc/work/pymol/draw_links.py \n"
    )
    out_file_contents += "# 3. Type: @[FILE_NAME.py] in the command line.\n"
    out_file_contents += (
        "# 4. Make sure the .py files are in the same directory as the pdb.\n"
    )

    # Now go through each residue pair.
    for interaction_pair, cylinder_radii in res_res_scores.items():
        res1, res2 = str(interaction_pair[0]), str(interaction_pair[1])
        feature_rep = (
            f"draw_links selection1=resi {res1}, "
            + f"selection2=resi {res2}, "
            + "color=red, "
            + f"radius={cylinder_radii} \n"
        )
        out_file_contents += feature_rep
    # Finally, group all cylinders made together,
    # (easier for user to handle in PyMOL)
    out_file_contents += "group All_Cylinders, link*\n"

    # Save file.
    out_file_safe = Path(out_file)
    with open(out_file_safe, "w+", encoding="utf-8") as file_out:
        file_out.write(out_file_contents)
    print(f"The file: {out_file_safe} was written to disk.")


def rescale_scores(
    input_dict: dict[tuple[int, int], float], max_value: float = 0.5
) -> dict[tuple[int, int], float]:
    """
    Rescale a dictionary containing per residue or residue-residue scores/counts etc..

    Parameters
    ----------
    input_dict : dict[tuple[int, int], float]
        Keys are the residue pairs, values are the associated value for the pair.
        Key formatting is a tuple of 2 integers, residue number 1 and residue number 2.

    max_value : float
        Rescale the values so that this is the max value in the returned dictionary
        Default = 0.5, good for PyMOL residue-residue connection representation.

    Returns
    ----------
    dict[tuple[int, int], float]
        Rescaled scores, has the same formatting as the input dictionary.
    """
    max_strength = max(list(input_dict.values()))
    scale_factor = max_strength / max_value

    rescaled_dict = {}
    for key, curr_value in input_dict.items():
        new_value = round((curr_value / scale_factor), 4)
        rescaled_dict.update({key: new_value})

    return rescaled_dict
