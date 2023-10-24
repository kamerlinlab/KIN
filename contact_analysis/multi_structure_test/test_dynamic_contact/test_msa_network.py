"""This file takes in contacts updated with the msa indexing,
and outputs a network of contacts shared among all the structures
along with their conservation scores. """

from itertools import chain
from collections import Counter
import glob
import os
from re import I
import numpy as np
import pandas as pd
import time
from tools_proj.pymol_projections import project_pymol_res_res_scores


def common_network(
    path_input: str,
    target_structure: str,
    contact_index="pdb",
    no_vdw=True,
    only_sc=False,
) -> tuple[dict, dict]:
    """The outermost function that takes in a path to all csv
    files with contacts after msa reindexing was performed.
    The output is a set of two dictionaries:
    first is a dictionary of contacts, where the keys are contact residues
    and a value is a conservation score
    (indexing type can be changed between msa and pdb of projected structure);
    second dictionary contains analogous contacts and matching colors that describe interaction type.
    """
    intputs = path_input + "/*.csv"
    msa_df_files = glob.glob(intputs)

    structure_count = 0
    interaction_count = 0
    all_interactions_dict = {}
    all_interactions_dfs = {}
    missing_res_dict = {}

    for file_path in msa_df_files:
        file_name = os.path.basename(file_path)
        system_name = file_name.split("_msa")[0]
        all_interactions_dict[system_name] = {}
        all_interactions_list = []

        structure_count += 1

        df = pd.read_csv(file_path)
        all_interactions_dfs[system_name] = df
        res1_msa_list = list(df["Res1_msa"])
        res2_msa_list = list(df["Res2_msa"])
        int_type_list = list(df["Interaction_Type"])
        int_location = list(df["Residue_Parts"])

        missing_res = all_interactions_dfs[system_name]["Missing_res_msa"]
        missing_res_list = [int(value) for value in missing_res if pd.notna(value)]
        missing_res_dict[system_name] = missing_res_list

        if system_name == target_structure:
            target_msa_pdb = {}
            res1_pdb_list = list(df["Res1_pdb"])
            res2_pdb_list = list(df["Res2_pdb"])
            for index, res1 in enumerate(res1_pdb_list):
                target_msa_pdb[(res1_msa_list[index], res2_msa_list[index])] = (
                    res1_pdb_list[index],
                    res2_pdb_list[index],
                )

        for index, res_1_msa in enumerate(df["Res1_msa"]):
            all_interactions_list.append((res_1_msa, res2_msa_list[index]))
        all_interactions_dict[system_name] = {}
        for index, contact in enumerate(all_interactions_list):
            all_interactions_dict[system_name][contact] = (
                int_type_list[index],
                int_location[index],
            )
    conservation_tem_msa_dr, colors_int_type = conservation_nextwork_dict(
        all_interactions_dict,
        missing_res_dict,
        target_msa_pdb,
        target_structure,
        contact_index,
        no_vdw,
        only_sc,
    )
    return conservation_tem_msa_dr, colors_int_type


def conservation_nextwork_dict(
    all_int_dict: dict,
    missing_res_dict: dict,
    target_msa_pdb_dict: dict,
    target_structure: str,
    index_type: str,
    exclude_vdw=True,
    only_sc=False,
) -> tuple[dict, dict]:
    """Takes in all the contacts in the form of a dictionary, compares it to the structure of the
    target to make sure that the contacts that are not present are not due to the missing residues,
    and outputs a dictionary of conservation scores in the desired indexing.
    Residue_Parts"""
    start_time = time.time()
    conservation = {}
    target_contacts_dict = all_int_dict[target_structure]
    colors = {}
    colors["hbond"] = "br1"
    colors["vdw"] = "green"
    colors["saltbridge"] = "dash"
    colors["hydrophobic"] = "br9"
    colors["pipi"] = "br5"
    colors["cationpi"] = "brightorange"
    conservation_int_type = {}
    for target_contacts, target_properties in target_contacts_dict.items():
        contact_yes = 0
        contact_no = 0
        contact_dna = 0
        total_structure = 0
        target_res1 = target_contacts[0]
        target_res2 = target_contacts[1]

        target_int_type = target_properties[0]
        if exclude_vdw is True and target_int_type == "vdw":
            continue
        if only_sc is True:
            target_int_location = target_properties[0]
            target_loc_1, target_loc_2 = target_int_location.split("-")
            if target_loc_1 != "sc" or target_loc_2 != "sc":
                continue
        for structure, contact_dict in all_int_dict.items():
            if structure != target_structure:
                print(structure)

                total_structure += 1
                missing_res_list = missing_res_dict[structure]
                if target_res1 in missing_res_list or target_res2 in missing_res_list:
                    contact_dna += 1
                    print("missing")
                    continue

                if (target_res1, target_res2) in contact_dict:
                    properties = contact_dict[(target_res1, target_res2)]
                    if exclude_vdw is True:
                        int_type = properties[0]
                        if int_type == "vdw":
                            continue
                    if only_sc is True:
                        int_location = properties[1]
                        loc_1, loc_2 = int_location.split("-")
                        if loc_1 != "sc" or loc_2 != "sc":
                            continue
                    contact_yes += 1

                elif (
                    target_res2,
                    target_res1,
                ) in contact_dict:
                    properties = contact_dict[(target_res2, target_res1)]
                    if exclude_vdw is True:
                        int_type = properties[0]
                        if int_type == "vdw":
                            continue
                    if only_sc is True:
                        int_location = properties[1]
                        loc_1, loc_2 = int_location.split("-")
                        if loc_1 != "sc" or loc_2 != "sc":
                            continue
                    contact_yes += 1
                else:
                    contact_no += 1
        conservation[(target_res1, target_res2)] = contact_yes / (
            contact_dna + contact_no + contact_yes
        )
        conservation_int_type[(target_res1, target_res2)] = colors[target_int_type]
        print(conservation)
    if index_type == "msa":
        dir_out = conservation
    elif index_type == "pdb":
        conservation_pdb = {}
        conservation_int_type_pdb = {}
        for contact, score in conservation.items():
            contact_pdb = target_msa_pdb_dict[contact]
            contact_pdb = (int(contact_pdb[0][3:]), int(contact_pdb[1][3:]))
            conservation_pdb[contact_pdb] = score
            conservation_int_type_pdb[contact_pdb] = conservation_int_type[contact]
        print(conservation_pdb)
        dir_out = conservation_pdb

    else:
        print()
        print(
            "ERROR: Incorrecect indexing type is specified for the convservation scores"
        )
        print("-----------------------------------------------------------")
        print()
        print(
            "Please specify what is the desiered index for the conservation map residues."
        )
        print(
            'If the indexing according to the pdb of a target structure is desiered set index_type = "pdb"'
        )
        print(
            'If conservation residues should be indexed according to msa indexing set index_type = "msa"'
        )
        print()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Function: conservation_nextwork_dict")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
    return dir_out, conservation_int_type_pdb


def conservation_nextwork_df(
    all_int_df: dict,
    target_msa_pdb_dict: dict,
    target_structure: str,
    index_type: str,
    exclude_vdw=True,
    only_sc=False,
) -> dict:
    """Takes in all the contacts in the form of a dictionary, compares it to the structure of the
    target to make sure that the contacts that are not present are not due to the missing residues,
    and outputs a dictionary of conservation scores in the desired indexing.
    """
    start_time = time.time()
    target_df = all_int_df[target_structure]
    conservation = {}
    for index, row in target_df.iterrows():
        contact_yes = 0
        contact_no = 0
        contact_dna = 0
        total_structure = 0
        target_res1_msa = row["Res1_msa"]
        target_res2_msa = row["Res2_msa"]
        if exclude_vdw is True and row["Interaction_Type"] == "vdw":
            continue

        if only_sc is True:
            int_location = row["Residue_Parts"]
            int_loc1, int_loc2 = int_location.split("-")
            if int_loc1 != "sc" or int_loc2 != "sc":
                continue

        for structure, structure_df in all_int_df.items():
            total_structure += 1
            if structure != target_structure:
                missing_res = [
                    int(value)
                    for value in structure_df["Missing_res_msa"]
                    if pd.notna(value)
                ]
                if target_res1_msa in missing_res or target_res2_msa in missing_res:
                    contact_dna += 1
                    continue
                if any(
                    (
                        (structure_df["Res1_msa"] == target_res1_msa)
                        & (structure_df["Res2_msa"] == target_res2_msa)
                    )
                    | (
                        (structure_df["Res2_msa"] == target_res1_msa)
                        & (structure_df["Res1_msa"] == target_res2_msa)
                    )
                ):
                    contact_yes += 1
                else:
                    contact_no += 1
        conservation[(target_res1_msa, target_res2_msa)] = contact_yes / (
            contact_dna + contact_no + contact_yes
        )
    if index_type == "msa":
        dir_out = conservation
    elif index_type == "pdb":
        dir_out = conservation
    else:
        print()
        print(
            "ERROR: Incorrecect indexing type is specified for the convservation scores"
        )
        print("-----------------------------------------------------------")
        print()
        print(
            "Please specify what is the desiered index for the conservation map residues."
        )
        print(
            'If the indexing according to the pdb of a target structure is desiered set index_type = "pdb"'
        )
        print(
            'If conservation residues should be indexed according to msa indexing set index_type = "msa"'
        )
        print()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Function: conservation_nextwork_df")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
    return dir_out


# CHECK IF FUNCTIONS ARE THE SAME
# conservation_tem_msa_df = conservation_nextwork_df(
#    all_interactions_dfs,
#    target_msa_pdb,
#    TARGET_STRUCTURE,
#    index_type="msa",
#    exclude_vdw=False,
# )
project_pymol_res_res_scores(
    conservation_tem_msa_dr, "Conservations_dynamic.pml", colors_int_type
)
quit()
if conservation_tem_msa_df.keys() == conservation_tem_msa_dr.keys():
    print("KEYS ARE THE SAME")
else:
    print("KEYS ARE DIFFERENT")
if np.allclose(
    np.array(list(conservation_tem_msa_df.values())),
    np.array(list(conservation_tem_msa_dr.values())),
    rtol=10e-7,
    atol=10e-7,
):
    print("VALUES ARE THE SAME")
else:
    print("VALUES ARE DIFFERENT")
    differences = {}
    for key, value in conservation_tem_msa_df.items():
        if value != conservation_tem_msa_dr[key]:
            differences[key] = abs(
                conservation_tem_msa_df[key] - conservation_tem_msa_dr[key]
            )
    print(differences)
quit()
# Combining filtered dataframes into a list of tuples,
# where each tuple is a contact based on msa indx
combined_data = list(
    chain.from_iterable(
        df_filtered.itertuples(index=False) for df_filtered in filtered_dfs
    )
)
pair_counts = Counter(combined_data)
selected_contacts = pd.DataFrame({"Res1_msa": [], "Res2_msa": []})
res1_selected = []
res2_selected = []

for pair, count in pair_counts.items():
    if count / structure_count >= THRESHOLD:
        interaction_count += 1
        res1_selected.append(pair[0])
        res2_selected.append(pair[1])
selected_contacts["Res1_msa"] = res1_selected
selected_contacts["Res2_msa"] = res2_selected

print(
    f"There are {interaction_count} interactions that occur in the {THRESHOLD*100}% of structures"
)
print(f"Total number of structures:{structure_count}")
print(f"This interaction occure in {structure_count*THRESHOLD} structures")

# Compare to the interactions of the TEM-1 and reduce the network only to
# the types of interactions present in TEM-1

for file_path in msa_df_files:
    df = pd.read_csv(file_path)
    merged_dataframe = pd.merge(selected_contacts, df, on=msa_columns)

    file_name = os.path.basename(file_path)
    file_name_without_extension = os.path.splitext(file_name)[0]

    NETWORK_OUTPUT = "network_output/" + file_name_without_extension + "_no_type.csv"
    merged_dataframe.to_csv(NETWORK_OUTPUT, index=False)

    if file_path.endswith("1M40_TEM-1_msa.csv"):
        TEM1_df = merged_dataframe[["Interaction_Type", "Res1_msa", "Res2_msa"]]


for file_path in network_files:
    df = pd.read_csv(file_path)

    merged_dataframe = pd.merge(
        TEM1_df, df, on=["Interaction_Type", "Res1_msa", "Res2_msa"]
    )
    file_name = os.path.basename(file_path)
    file_name_without_extension = os.path.splitext(file_name)[0]
    print(
        file_name,
        ": preserved interactions of TEM type",
        merged_dataframe.shape[0],
    )
    NETWORK_OUTPUT = (
        "network_output/proj_1M40_TEM-1/" + file_name_without_extension + ".csv"
    )
    merged_dataframe.to_csv(NETWORK_OUTPUT, index=False)
