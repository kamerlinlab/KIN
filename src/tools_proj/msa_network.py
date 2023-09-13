"""This file takes in contacts updated with the msa indexing,
and outputs a network of contacts shared among all the structures
along with their conservation scores. """

import glob
import os
import time
import csv
import ast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def common_network(
    path_input: str,
    target_structure: str,
    network_index="pdb",
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
        network_index,
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


def conservation_nextwork_df(
    all_int_df: dict,
    target_msa_pdb_dict: dict,
    target_structure: str,
    index_type: str,
    exclude_vdw=True,
    only_sc=False,
) -> dict:
    """Takes in all the contacts in the form of a data framework,
    the workflow is analagous to the function above but 5 times slower.
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
        conservation_pdb = {}
        for contact, score in conservation.items():
            contact_pdb = target_msa_pdb_dict[contact]
            contact_pdb = (int(contact_pdb[0][3:]), int(contact_pdb[1][3:]))
            conservation_pdb[contact_pdb] = score
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
    print("Function: conservation_nextwork_df")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
    return dir_out


# Following are analysis functions for the network of contacts
# TODO: write function desccriptions
def get_contacts_from_csv(csv_file_path, value_type=float):
    data = {}
    with open(csv_file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key, value in row.items():
                key_float = ast.literal_eval(key)
                if value_type == float:
                    data[key_float] = float(value)
                else:
                    data[key_float] = value
    return data


def make_grid(data, total_res_number):
    grid = np.zeros((total_res_number + 1, total_res_number + 1))
    for index, (key, value) in enumerate(data.items()):
        x = key[0]
        y = key[1]
        grid[x][y] = value
        grid[y][x] = value
    return grid


def difference_matrix(
    static_network,
    static_colors,
    dynamic_network,
    dynamic_colors,
    diff_threshold=0.0,
    only_overlap=False,
    color_type="int",
):
    diff_network = {}
    diff_colors = {}
    counter_only_md = 0
    counter_only_crystal = 0
    counter_difference = 0
    diff_list = []

    for key, value in static_network.items():
        if (key[0], key[1]) in dynamic_network or (key[1], key[0]) in dynamic_network:
            diff_value = abs(value - dynamic_network[key])
            if diff_value > diff_threshold:
                counter_difference += 1
                diff_network[key] = diff_value
                diff_colors[key] = static_colors[key]
                diff_list.append(diff_network[key])
        if only_overlap:
            continue

        elif (
            (key[0], key[1]) not in dynamic_network
            and (key[1], key[0]) not in dynamic_network
            and value > diff_threshold
        ):
            diff_network[key] = value
            counter_only_crystal += 1
            if color_type == "int":
                diff_colors[key] = static_colors[key]
            else:
                diff_colors[key] = "hotpink"
            diff_list.append(diff_network[key])
    if not only_overlap:
        for key, value in dynamic_network.items():
            if (
                (key[0], key[1]) not in static_network
                and (key[1], key[0]) not in static_network
                and value > diff_threshold
            ):
                diff_network[key] = value
                counter_only_md += 1
                if color_type == "int":
                    diff_colors[key] = dynamic_colors[key]
                else:
                    diff_colors[key] = "green"
                diff_list.append(diff_network[key])
    print("Total number of contacts in the difference network:", len(diff_network))
    print("Number of only MD contacts:", counter_only_md)
    print("Number of only crystal contacts:", counter_only_crystal)
    return diff_network, diff_colors, diff_list


def plot_int_map(grid, title, threshold=0.1):
    x_coords, y_coords = np.meshgrid(np.arange(grid.shape[0]), np.arange(grid.shape[1]))
    x_coords = x_coords.flatten()
    y_coords = y_coords.flatten()

    cmap = plt.cm.Reds

    fig, ax = plt.subplots()
    above_threshold_points = []

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] > threshold:
                above_threshold_points.append((j, i, grid[i, j]))

    x_coords, y_coords, values = zip(*above_threshold_points)
    x_coords, y_coords, values = (
        np.array(x_coords),
        np.array(y_coords),
        np.array(values),
    )
    cmap = plt.cm.get_cmap("Reds")
    normalize = plt.Normalize(0.1, 1)
    scatter = ax.scatter(
        x_coords, y_coords, c=values, cmap=cmap, norm=normalize, marker="s", s=10
    )

    cbar = plt.colorbar(scatter)
    cbar.set_label("Contact Value")

    ax.grid(which="both", color="black", linestyle="--", linewidth=0.5, alpha=0.5)
    ax.set_aspect("equal")
    plt.title(title)
    ax.set_xlabel("Residue Index")
    ax.set_ylabel("Residue Index")

    plt.show()


def plot_hist_of_contacts(contact, title, filename, color_choice="blue"):
    contact_score_list = []
    for key, value in contact.items():
        contact_score_list.append(value)
    plt.hist(
        contact_score_list, bins=10, alpha=0.7, color=color_choice, edgecolor="black"
    )

    plt.xlabel("Conservation scores")
    plt.ylabel("Frequency")
    plt.title(title)
    plt.grid(axis="y", linestyle="--", alpha=0.9)
    plt.show()
    # plt.savefig(filename)
