"""
Module that helps find alternative contact combinations given a pair of residues
belonging to a target protein.

This can therefore be used to suggest single or double mutations for
a given target protein.
"""
import re
import pandas as pd

AMBER_3_LETTER_AA_TO_1 = {
    "ALA": "A",
    "ARG": "R",
    "ASN": "N",
    "ASH": "D",
    "ASP": "D",
    "CYS": "C",
    "CYX": "C",
    "CYM": "C",
    "GLN": "Q",
    "GLU": "E",
    "GLH": "E",
    "GLY": "G",
    "HIS": "H",
    "HIE": "H",
    "HID": "H",
    "HIP": "H",
    "ILE": "I",
    "LEU": "L",
    "LYS": "K",
    "LYN": "K",
    "MET": "M",
    "PHE": "F",
    "PRO": "P",
    "SER": "S",
    "THR": "T",
    "TRP": "W",
    "TYR": "Y",
    "VAL": "V",
}


def find_equivalent_contacts(
    all_msa_contacs_dfs: dict[str, pd.DataFrame],
    target_res_pair: tuple[int, int],
    target_msa_seq: str,
    no_vdws: bool,
) -> tuple[dict[str, int], dict[str, tuple[str, int, int]]]:
    """
    Given a target protein and a pair of residues in that target protein, find all
    other proteins that have that contact pair.
    Returns two dictionaries

    Parameters
    ----------
    all_msa_contacs_dfs: dict[str, pd.DataFrame],
        dictionary of dataframes, with keys being each protein.
        Values are a dataframe of contacts data for each protein.

    target_res_pair: tuple[int, int]
        Residue numbers of the pair of residues that form a contact in the protein of interest.
        This is the pdb numbering, i.e. not the msa numbering.

    target_msa_seq: str
        msa sequence for the target protein.

    no_vdws: bool
        If set to True, interactions of type "vdws" will not be included in the calculation.

    Returns
    ----------
    contact_combinations: dict[str, int]
        Different types of interactions formed between the residue pair and their frequency.
        Each key is a string describing the type of contact.
        Each value refers to the number of observations of that contact.

    contact_examples: dict[str, tuple[str, int, int]]
        Examples of the different types of interactions formed between the residue pair.
        Each key is a string describing the type of contact.
        Each value is a tuple containing the protein name, and both residues involved.
    """
    msa_to_pdb_converter = _create_pdb_to_msa_converter(msa_sequence=target_msa_seq)

    # convert to msa numbering for the residue pair.
    target_msa_pair = (
        msa_to_pdb_converter[target_res_pair[0]],
        msa_to_pdb_converter[target_res_pair[1]],
    )

    detailed_contact_info = []
    for protein, msa_contacs_df in all_msa_contacs_dfs.items():
        results = msa_contacs_df[
            (msa_contacs_df["Res1_msa"] == target_msa_pair[0])
            & (msa_contacs_df["Res2_msa"] == target_msa_pair[1])
        ]

        if results.empty:
            continue

        res1_pdb = results["Res1_pdb"].values[0]
        res2_pdb = results["Res2_pdb"].values[0]

        res1_numb = re.search(r"\d+", res1_pdb).group()
        res1_name = re.search(r"[a-zA-z]+", res1_pdb).group()
        res2_numb = re.search(r"\d+", res2_pdb).group()
        res2_name = re.search(r"[a-zA-z]+", res2_pdb).group()

        interaction_type = results["Interaction_Type"].values[0]
        residue_parts = results["Residue_Parts"].values[0]

        if no_vdws:
            if interaction_type == "vdw":
                continue

        detailed_contact_info.append(
            {
                "protein": protein,
                "res1_numb": res1_numb,
                "res1_name": res1_name,
                "res2_numb": res2_numb,
                "res2_name": res2_name,
                "interaction_type": interaction_type,
                "residue_parts": residue_parts,
            }
        )

    contact_combinations, contact_examples = {}, {}
    for contact in detailed_contact_info:
        res1_name, res2_name = contact["res1_name"], contact["res2_name"]
        interaction_type = contact["interaction_type"]
        residue_parts = contact["residue_parts"]

        contact_description = (
            f"{res1_name} {res2_name} {interaction_type} {residue_parts}"
        )

        if contact_description not in contact_combinations:
            contact_combinations[contact_description] = 0
            contact_examples[contact_description] = []

        contact_combinations[contact_description] += 1
        contact_examples[contact_description].append(
            (contact["protein"], contact["res1_numb"], contact["res2_numb"])
        )

    contact_combinations = dict(
        sorted(contact_combinations.items(), key=lambda item: item[1], reverse=True)
    )

    return contact_combinations, contact_examples


def find_possible_single_point_mutations(
    contact_combinations: dict[str, int],
    target_res_pair: tuple[int, int],
    target_prot_seq: list[str],
    conservation_cutoff: int = 3,
) -> list[dict]:
    """
    Given a dictionary of residue pairs in contact, find all possible single point mutations
    that can be made.

    Parameters
    ----------
    contact_combinations: dict[str, int]
        Different types of interactions formed between a residue pair and their frequency.
        Each key is a string describing the type of contact.
        Each value refers to the number of observations of that contact.

    target_res_pair: tuple[int, int]
        The residue numbers of the contact for the target protein.

    target_prot_seq: list[str]
        One letter amino acid sequence of the target protein.

    conservation_cutoff: int = 3,
        The minimum number of proteins the contact needs to have been observed in to be considered.
        Default = 3.

    Returns
    ----------
    list[dict]
        List of mutations to try. Each list item is a different mutation.
        Each list item is a dictionary containing information about the mutation.
    """
    res1_numb, res2_numb = target_res_pair
    target_res1_aa = target_prot_seq[res1_numb - 1]  # 0-indexed
    target_res2_aa = target_prot_seq[res2_numb - 1]  # 0-indexed

    mutations_to_try = []
    for contact, conservation in contact_combinations.items():
        contact_info = contact.split()
        res1_3letter, res2_3letter = contact_info[0:2]
        res1_aa, res2_aa = (
            AMBER_3_LETTER_AA_TO_1[res1_3letter],
            AMBER_3_LETTER_AA_TO_1[res2_3letter],
        )

        if (res1_aa == target_res1_aa) and (res2_aa == target_res2_aa):
            continue  # same as WT
        if (res1_aa != target_res1_aa) and (res2_aa != target_res2_aa):
            continue  # can only test single point mutants.
        if conservation < conservation_cutoff:
            continue

        # add the single mutation info
        if res1_aa != target_res1_aa:
            mutation_info = {
                "res_numb": res1_numb,
                "wt_res": target_res1_aa,
                "mutated_res": res1_aa,
            }
        else:  # res2 to mutate instead..
            mutation_info = {
                "res_numb": res2_numb,
                "wt_res": target_res2_aa,
                "mutated_res": res2_aa,
            }

        if mutation_info in mutations_to_try:
            continue  # if already included from a prior observation.
        mutations_to_try.append(mutation_info)

    return mutations_to_try


def find_possible_double_mutations(
    contact_combinations, target_res_pair: tuple[int, int], target_prot_seq
) -> list[dict]:
    """
    Given a dictionary of residue pairs in contact, find all possible double mutations
    that can be made.
    Parameters
    ----------
    contact_combinations: dict[str, int]
        Different types of interactions formed between a residue pair and their frequency.
        Each key is a string describing the type of contact.
        Each value refers to the number of observations of that contact.

    target_res_pair: tuple[int, int]
        The residue numbers of the contact for the target protein.

    target_prot_seq: list[str]
        One letter amino acid sequence of the target protein.

    conservation_cutoff: int = 3,
        The minimum number of proteins the contact needs to have been observed in to be considered.
        Default = 3.

    Returns
    ----------
    list[dict]
        List of mutations to try. Each list item is a different double mutation.
        Each list item is a dictionary containing information about the double mutation.
    """
    res1_numb, res2_numb = target_res_pair
    target_res1_aa = target_prot_seq[res1_numb - 1]  # 0-indexed
    target_res2_aa = target_prot_seq[res2_numb - 1]  # 0-indexed

    mutations_to_try = []
    for contact, conservation in contact_combinations.items():
        contact_info = contact.split()
        res1_3letter, res2_3letter = contact_info[0:2]
        res1_aa, res2_aa = (
            AMBER_3_LETTER_AA_TO_1[res1_3letter],
            AMBER_3_LETTER_AA_TO_1[res2_3letter],
        )

        # only looking for double mutants.
        if (res1_aa == target_res1_aa) or (res2_aa == target_res2_aa):
            continue
        if conservation < 3:
            continue  # only test those with 3 or more observations.

        # add the double mutation info
        mutation_info = {
            "res1_numb": res1_numb,
            "wt_res1": target_res1_aa,
            "mutated_res1": res1_aa,
            "res2_numb": res2_numb,
            "wt_res2": target_res2_aa,
            "mutated_res2": res2_aa,
        }
        if mutation_info in mutations_to_try:
            continue  # if already included from prior observation.
        mutations_to_try.append(mutation_info)

    return mutations_to_try


def _create_pdb_to_msa_converter(msa_sequence: str) -> dict[int, int]:
    """
    Create a dictionary that can enable easily converting
    between pdb and msa numbers given an msa_sequence.

    Parameters
    ----------
    msa_sequence: str
        msa sequence of the target protein.

    Returns
    ----------
    dict[int, int]
        key is the pdb residue number, value is the msa residue number.
    """
    curr_msa_number, curr_pdb_numb = 0, 0
    index_pdb_msa = {}
    for msa_residue in msa_sequence:
        if msa_residue == "*":
            continue
        if msa_residue == "-":
            curr_msa_number += 1
        else:
            curr_msa_number += 1
            curr_pdb_numb += 1

            index_pdb_msa[curr_pdb_numb] = curr_msa_number
    return index_pdb_msa
