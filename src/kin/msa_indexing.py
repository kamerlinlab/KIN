"""Following code adds the msa-based indexing to both residues of each contact"""

import warnings
import pandas as pd
import numpy as np


def parse_fasta(file_path):
    """Takes in a msa alignment produced by modeller in fasta formating and
    outputs a sequence as string with '-' for the gaps introduced by msa"""
    sequences = {}
    current_name = None
    current_sequence = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line.startswith(">"):
                if current_name is not None:
                    sequences[current_name] = "".join(current_sequence)
                    current_sequence = []

                current_name = line[1:]
            else:
                current_sequence.append(line)

        # Add the last sequence to the dictionary
        if current_name is not None:
            sequences[current_name] = "".join(current_sequence)

    return sequences


def indexing_pdb_to_msa(
    msa_sequence: list[str], df_input: pd.DataFrame
) -> pd.DataFrame:
    """This funciton takes in the msa sequence and a dataframe of the
    pdb contact analysis output, updates original dataframe with the new
    columns that contain msa indexing and returns it

    TODO: flip the order such that msa indexing are first and second columns
    """

    res1_list = list(df_input["Res1"])
    res2_list = list(df_input["Res2"])
    counter = 0.0
    index_pdb_msa = {}
    msa_indx_res1 = []
    msa_indx_res2 = []
    missing_indicies = []

    for i, res in enumerate(msa_sequence):
        if res != "-":
            counter += 1
            index_pdb_msa[int(counter)] = i + 1
        else:
            missing_indicies.append(i + 1)
    for res_counter, res1 in enumerate(res1_list):
        pdb_indx_res1 = res1[3:]
        res2 = res2_list[res_counter]
        pdb_indx_res2 = res2[3:]
        msa_indx_res1.append(index_pdb_msa[int(pdb_indx_res1)])
        msa_indx_res2.append(index_pdb_msa[int(pdb_indx_res2)])

    df_input["Res1_msa"] = msa_indx_res1
    df_input["Res2_msa"] = msa_indx_res2
    # Reshufle the columns such that the msa indexing follows the pdb indexing
    #  and rename the pdb indexing columns
    new_names = [
        "Res1_pdb",
        "Res2_pdb",
        "Interaction_Type",
        "Residue_Parts",
        "Res1_msa",
        "Res2_msa",
    ]
    df_input.columns = new_names
    new_order = [
        "Res1_pdb",
        "Res2_pdb",
        "Res1_msa",
        "Res2_msa",
        "Interaction_Type",
        "Residue_Parts",
    ]
    df_input = df_input[new_order]
    # Make a df column with all missing residues and the rest of them fill in with Nan
    missing_indicies_index = range(len(missing_indicies))
    # In this case, it is okay.
    pd.options.mode.chained_assignment = None  # default = warn
    df_input["Missing_res_msa"] = np.nan
    df_input.loc[missing_indicies_index, "Missing_res_msa"] = missing_indicies
    df_input["Missing_res_msa"] = df_input["Missing_res_msa"].astype(pd.Int64Dtype())
    return df_input


def clean_up_sequence(
    seq_dict: dict, target_protein: str
) -> tuple[list[str], list[str]]:
    """Function takes in a dictionary of sequences, pickes out one that match a target protein
    and cleans it according to the notation used in the contacts"""
    raw_msa_sequence = seq_dict.get(target_protein)
    residue_map = {
        "A": "ALA",
        "R": "ARG",
        "D": "ASP",
        "N": "ASN",
        "C": "CYS",
        "E": "GLU",
        "Q": "GLN",
        "G": "GLY",
        "H": "HIS",
        "I": "ILE",
        "L": "LEU",
        "K": "LYS",
        "M": "MET",
        "F": "PHE",
        "P": "PRO",
        "S": "SER",
        "T": "THR",
        "W": "TRP",
        "Y": "TYR",
        "V": "VAL",
        "-": "-",
    }
    raw_msa_sequence = raw_msa_sequence.replace("*", "")
    short_sequence = raw_msa_sequence.replace("-", "")

    short_sequence_list = list(short_sequence)
    sequence_list = list(raw_msa_sequence)
    sequence = [residue_map[res] for res in sequence_list]
    short_sequence = [residue_map[res] for res in short_sequence_list]

    return sequence, short_sequence


def parse_contact_output(
    pdb_file: str, contact_type: str, retention_percent=0.5
) -> pd.DataFrame:
    """This function takes in a raw output of dynamic or crystal structure contacts and
    returns it as a dataframe that can be used by msa conversion function.
    In the case of the dynamic contacts, the resutls are counted such that if the contact appears in
    X percent of simluation time it counts as 1,
    otherwhile it is not preserved enough and counts as 0.

    TODO: repace forloop with a df function if slow
    """

    if contact_type == "md":
        df_in = pd.read_csv(pdb_file, delimiter=",")
        df_out = pd.DataFrame()
        res_1_list = []
        res_2_list = []
        int_type_list = []
        location_list = []
        number_of_frames = df_in.shape[0]

        for name, time_contacts in df_in.items():
            res_1_val, res_2_val, int_type_val, location_val = name.split(" ")
            counter = 0
            for frame in time_contacts:
                if frame == 1:
                    counter += 1

            if counter >= number_of_frames * retention_percent:
                res_1_list.append(res_1_val)
                res_2_list.append(res_2_val)
                int_type_list.append(int_type_val)
                location_list.append(location_val)

        df_out["Res1"] = res_1_list
        df_out["Res2"] = res_2_list
        df_out["Interaction_Type"] = int_type_list
        df_out["Residue_Parts"] = location_list

    elif contact_type == "crystal":
        df_out = pd.read_csv(pdb_file, delimiter=" ")
        df_out = df_out.dropna(axis=1)
    else:
        print()
        print("ERROR: Incorrect type of contact data is speciefied")
        print("----------------------------------------------------")
        print()
        print('If using crystal structure - please specify contact_type = "crystal";')
        print('and if using md data - please specify contact_type = "md".')
        print()
        exit()

    return df_out


############################################################################
