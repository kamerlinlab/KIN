"""
A collection of useful functions that have no specific home.

Functions included are:
1. open_many_single_frame_contacts_files()
    Open a number of single frame contact analysis files.

2. normalise_dict_values()
    Normalise a set of dictionary values to have max value of 1.

3. per_residue_distance_to_site()
    Calculate the closest heavy atom distance of each residue to a specific site
"""
from typing import Optional, Any
import warnings
from pathlib import Path
import csv

import numpy as np
import MDAnalysis as mda
from MDAnalysis.analysis import distances


def open_many_single_frame_contacts_files(
    folder_path: str, protein_names: list[str]
) -> dict[str, list[str]]:
    """
    Open a number of single frame contact analysis files.
    Assumes all files are saved in the same directory with the following format:
    "{protein_name}_contacts.txt"

    Parameters
    ----------
    folder_path: str
        Path to the folder where all the contacts are stored.

    protein_names: list[str]
        list of protein names/structures to open.

    Returns
    ----------
    dict[str, list[str]]
        keys are the name of each protein.
        Values are a list of the interactions found.
    """
    all_protein_contacts = {}
    for protein in protein_names:
        file_name = f"{protein}_contacts.txt"
        file_path = Path(folder_path, file_name)

        with open(file_path, "r", encoding="utf-8") as file_in:
            prot_contacts = []
            for line in list(file_in)[1:]:  # skip header.
                prot_contacts.append(line.strip())

        all_protein_contacts[protein] = prot_contacts

    return all_protein_contacts


def normalise_dict_values(original_dict: dict[Any, float]) -> dict[Any, float]:
    """
    Normalise a set of dictionary values to have max value of 1.
    Returns the dictionary without modifying the keys.

    Parameters
    ----------
    original_dict: dict[Any, float]
        dictionary to normalise

    Returns
    ----------
    dict[Any, float]
        normalised dictionary
    """
    max_score = max((original_dict.values()))

    updated_dict = {}
    for key, value in original_dict.items():
        new_score = value / max_score
        updated_dict[key] = new_score

    return updated_dict


def per_residue_distance_to_site(
    pdb_file: str,
    site_defintion: str,
    first_residue: int,
    last_residue: int,
    side_chain_only: bool = False,
    out_file: Optional[str] = None,
) -> dict:
    """
    Taken directly from https://github.com/kamerlinlab/KIF
    Calculate the closest heavy atom distance of each residue to an MDAnalysis defined
    selection of a site of interest. You can write the results to file if desired.

    Parameters
    ----------
    pdb_file : str
        Path to pdb file to use for the distance calculation.

    site_defintion : str
        MDAnalysis compatable defintion of the site of interest
        (i.e. could describe a binding site, active site etc..)
        See here for help: https://docs.mdanalysis.org/stable/documentation_pages/selections.html

    first_residue : int
        First residue to measure the distance from.

    last_residue : int
        Last residue to measure the distance to.

    side_chain_only: bool = False,
        Choose whether you want to measure the minimum distance using only the
        side chain of each residue. If true, only the side chain atoms are used.
        For glycines (no side chain), the CA of the glycine is used instead.

    out_file : Optional[str]
        Path to output file to write out data.
        If none provided, no file will be written.

    Returns
    ----------
    dict
        Residue numbers are the keys and minimum distances are the values.
    """
    # not requred for this type of analysis.
    warnings.filterwarnings("ignore", message="Element information is missing")

    universe = mda.Universe(pdb_file)
    group2 = universe.select_atoms(site_defintion)
    min_dists = {}

    if side_chain_only:
        for residue in range(first_residue, last_residue + 1):
            selection_str = "not backbone and not name H* and resid " + str(residue)
            group1 = universe.select_atoms(selection_str)

            res_dist_arr = distances.distance_array(
                group1.positions, group2.positions, box=universe.dimensions
            )

            try:
                min_res_dist = np.round(res_dist_arr.min(), 2)

            # catches "zero-size array to reduction operation minimum which has no identity"
            except ValueError:
                # This happens for glycines which have no side chain...
                selection_str = "name CA and resid " + str(residue)
                group1 = universe.select_atoms(selection_str)

                res_dist_arr = distances.distance_array(
                    group1.positions, group2.positions, box=universe.dimensions
                )

                min_res_dist = np.round(res_dist_arr.min(), 2)

            min_dists.update({residue: min_res_dist})

    else:  # both side and main chain route.
        for residue in range(first_residue, last_residue + 1):
            selection_str = "not name H* and resid " + str(residue)
            group1 = universe.select_atoms(selection_str)

            res_dist_arr = distances.distance_array(
                group1.positions, group2.positions, box=universe.dimensions
            )

            min_res_dist = np.round(res_dist_arr.min(), 2)
            min_dists.update({residue: min_res_dist})

    if out_file is None:
        return min_dists

    with open(out_file, "w", newline="", encoding="utf-8") as file_out:
        csv_out = csv.writer(file_out)
        csv_out.writerow(["Residue Number", "Minimum Distance"])
        csv_out.writerows(min_dists.items())
        print(f"{out_file} written to disk.")
    return min_dists
