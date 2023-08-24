"""
A collection of useful functions that have no specific home.
"""
from pathlib import Path


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
