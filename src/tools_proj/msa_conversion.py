"""
This module contains useful functions to add or swap back and forth between
the pdb (protein data bank) and msa (multiple sequence alingment) numbering systems
for each protein.
"""
import re


def add_msa_numbering_to_interaction_data(
    to_convert: list[str], msa_sequence: list[str]
) -> list[str]:
    """
    Append to every string in a list of interactions the msa numbers for both residues involved.
    Input interaction str format is as follows:
    [residue 1] [residue 2] [interaction type] [part(s) of residue involved]

    Output interaction str format is as follows:
    [All parts from input interaction] [msa numb residue 1] [msa numb residue 2]

    Parameters
    ----------
    to_convert: list[str]
        list of interactions to convert.

    msa_sequence: list[str]
        msa sequence for the given protein.

    Returns
    ----------
    list[str]
        list of interactions with msa numbering added.
    """
    # generate a pdb numbering to msa numbering conversion dict.
    curr_msa_number, curr_pdb_numb = 0, 0
    index_pdb_msa = {}
    for msa_residue in msa_sequence:
        if msa_residue == "-":
            curr_msa_number += 1
        else:
            curr_msa_number += 1
            curr_pdb_numb += 1

            index_pdb_msa[curr_pdb_numb] = curr_msa_number

    # now update each interaction label.
    converted_interactions = []
    for prot_interaction in to_convert:
        # extract the residue numbers from the string.
        split_parts = re.split(r"([a-zA-Z\s]+)", prot_interaction)
        split_parts = [part for part in split_parts if part]
        res1_numb, res2_numb = int(split_parts[1]), int(split_parts[3])

        # determine + append msa numbering scheme.
        msa_res1_numb, msa_res2_numb = (
            index_pdb_msa[res1_numb],
            index_pdb_msa[res2_numb],
        )
        new_label = f"{prot_interaction} {msa_res1_numb} {msa_res2_numb}"

        converted_interactions.append(new_label)
    return converted_interactions
