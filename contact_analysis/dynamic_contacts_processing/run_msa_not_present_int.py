"""This file takes in contacts updated with the msa indexing,
and outputs a network of contacts shared among all the structures
along with their conservation scores. """

from ctypes import Union
import glob
import os
from re import I
import time
import csv
import ast
from collections import Counter

from typing import Union, Dict, Tuple
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tools_proj.pymol_projections import project_pymol_res_res_scores

input_fiels = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/msa_index_contacts/retention_10"
projection_output = "1M40_TEM-1_network_10.pml"
contact_index = "pdb"


def common_network(
    path_input: str,
    target_structure: str,
    network_index="pdb",
    missing_network=False,
    no_vdw=True,
    only_sc=False,
) -> tuple[dict, dict, dict, pd.DataFrame]:
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
        network_index,
        no_vdw,
        only_sc,
    )
    if missing_network:
        (
            missing_contacts,
            missing_contacts_colors,
            missing_contacts_properties,
        ) = missing_contacts_dict(
            all_interactions_dict,
            target_structure,
            structure_count,
            no_vdw,
            only_sc,
        )
    else:
        missing_contacts = {}
        missing_contacts_colors = {}
        missing_contacts_properties = pd.DataFrame()
    return (
        conservation_tem_msa_dr,
        colors_int_type,
        missing_contacts,
        missing_contacts_colors,
        missing_contacts_properties,
    )


def missing_contacts_dict(
    all_interactions_dict: dict,
    target_structure: str,
    structure_count: int,
    no_vdw=True,
    only_sc=False,
) -> tuple[dict, dict, pd.DataFrame]:
    colors = {}
    colors["hbond"] = "br1"
    colors["vdw"] = "green"
    colors["saltbridge"] = "dash"
    colors["hydrophobic"] = "br9"
    colors["pipi"] = "br5"
    colors["cationpi"] = "brightorange"
    missing_contacts_count = {}
    missing_contacts_properties = pd.DataFrame(
        columns=(
            "Contact",
            "Count",
            "Interaction_Type",
            "Int_Type_Count",
            "Location",
            "Location_Count",
        )
    )
    missing_contacts = {}
    missing_contacts_colors = {}
    target_contacts_dict = all_interactions_dict[target_structure]
    for structure, contact_dict in all_interactions_dict.items():
        if structure != target_structure:
            for contact, _ in contact_dict.items():
                if (contact[0], contact[1]) not in target_contacts_dict and (
                    contact[1],
                    contact[0],
                ) not in target_contacts_dict:
                    if contact not in missing_contacts_count:
                        missing_contacts_count[contact] = 1
                    else:
                        missing_contacts_count[contact] += 1
    counter = 0
    int_type_list = []
    int_type_count_list = []
    location_list = []
    location_count_list = []
    for contact, value in missing_contacts_count.items():
        int_type = []
        location = []
        for structure, contact_dict in all_interactions_dict.items():
            if structure != target_structure:
                if contact in contact_dict:
                    int_type.append(contact_dict[contact][0])
                    location.append(contact_dict[contact][1])
        int_type_count = Counter(int_type)
        location_count = Counter(location)
        common_int_type = int_type_count.most_common(1)[0][0]
        count_int_type = int_type_count.most_common(1)[0][1]

        common_location = location_count.most_common(1)[0][0]
        count_location = location_count.most_common(1)[0][1]

        if no_vdw:
            if common_int_type == "vdw":
                continue
        if only_sc:
            location = common_location.split("-")
            if location[0] != "sc" or location[1] != "sc":
                continue
        counter += 1
        missing_contacts[contact] = value / structure_count
        missing_contacts_colors[contact] = colors[common_int_type]
        int_type_list.append(common_int_type)
        int_type_count_list.append(count_int_type / len(int_type))
        location_list.append(common_location)
        location_count_list.append(count_location / len(location))

    missing_contacts_properties["Contact"] = missing_contacts.keys()
    missing_contacts_properties["Count"] = missing_contacts.values()
    missing_contacts_properties["Interaction_Type"] = int_type_list
    missing_contacts_properties["Int_Type_Count"] = int_type_count_list
    missing_contacts_properties["Location"] = location_list
    missing_contacts_properties["Location_Count"] = location_count_list

    return missing_contacts, missing_contacts_colors, missing_contacts_properties


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
                total_structure += 1
                missing_res_list = missing_res_dict[structure]
                if target_res1 in missing_res_list or target_res2 in missing_res_list:
                    contact_dna += 1
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
    if index_type == "msa":
        dir_out = conservation
        colors_int_type = conservation_int_type
    elif index_type == "pdb":
        conservation_pdb = {}
        conservation_int_type_pdb = {}
        for contact, score in conservation.items():
            contact_pdb = target_msa_pdb_dict[contact]
            contact_pdb = (int(contact_pdb[0][3:]), int(contact_pdb[1][3:]))
            conservation_pdb[contact_pdb] = score
            conservation_int_type_pdb[contact_pdb] = conservation_int_type[contact]
        dir_out = conservation_pdb
        colors_int_type = conservation_int_type_pdb

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
    return dir_out, colors_int_type


(
    conservation_tem_msa,
    colors_int_type,
    miss_contact,
    miss_contact_colors,
    miss_contact_properties,
) = common_network(
    input_fiels,
    "1M40_TEM-1",
    contact_index,
    missing_network=True,
    no_vdw=True,
    only_sc=False,
)


counter_50 = 0
counter_90 = 0
counter_99 = 0
for key, value in conservation_tem_msa.items():
    if value >= 0.5:
        counter_50 += 1
    if value >= 0.9:
        counter_90 += 1
    if value >= 0.99:
        counter_99 += 1

print("Number of contacts with conservation score >= 0.5: ", counter_50)
print("Number of contacts with conservation score >= 0.9: ", counter_90)
print("Number of contacts with conservation score >= 0.99: ", counter_99)
print(miss_contact_colors)
print(type(miss_contact_colors))
quit()
project_pymol_res_res_scores(miss_contact, "tem1_missing_10.pml", miss_contact_colors)
# with open(output_filename, "w", newline="") as csvfile:
# csv_writer = csv.DictWriter(csvfile, fieldnames=conservation_tem_msa.keys())
# csv_writer.writeheader()
# csv_writer.writerow(conservation_tem_msa)

# if contact_index == "pdb":
# with open(colors_file, "w", newline="") as csvfile:
# csv_writer = csv.DictWriter(csvfile, fieldnames=colors_int_type.keys())
# csv_writer.writeheader()
# csv_writer.writerow(colors_int_type)
