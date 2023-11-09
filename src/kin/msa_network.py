"""This file takes in contacts updated with the msa indexing,
and outputs a network of contacts shared among all the structures
along with their conservation scores. """

import glob
import os
import time
import csv
import ast
from matplotlib.font_manager import font_scalings
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from pyparsing import col
from kin.msa_indexing import parse_fasta


def common_network(
    path_msa_alignment: str,
    path_input: str,
    target_structure: str,
    network_index="pdb",
    conservation_uniform=True,
    missing_network=False,
    no_vdw=True,
) -> tuple[dict, dict, pd.DataFrame, dict, dict, pd.DataFrame]:
    """The outermost function that takes in a path to all csv
    files with contacts after msa reindexing was performed.
    The output is a set of two dictionaries:
    first is a dictionary of contacts, where the keys are contact residues
    and a value is a conservation score
    (indexing type can be changed between msa and pdb of projected structure);
    second dictionary contains analogous contacts and matching colors that describe interaction type.
    """
    print("Target structure is:", target_structure)
    target_sequence = parse_fasta(path_msa_alignment)[target_structure]
    full_msa_pdb_index = {}
    counter = 0
    for i, res in enumerate(target_sequence):
        if res != "-":
            counter += 1
            full_msa_pdb_index[i + 1] = int(counter)
        else:
            full_msa_pdb_index[i + 1] = None

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
        if no_vdw is True:
            df = df[df["Interaction_Type"] != "vdw"]
        # if only_sc is True:
        #     df = df[df["Residue_Parts"] != "mc-mc"]

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
    conservation_tem_msa_dr, colors_int_type, properties = conservation_nextwork_dict(
        all_interactions_dict,
        missing_res_dict,
        target_msa_pdb,
        target_structure,
        network_index,
        conservation_uniform,
    )
    if missing_network:
        (
            missing_contacts,
            missing_contacts_colors,
            missing_contacts_properties,
        ) = missing_contacts_dict(
            all_interactions_dict,
            target_structure,
            full_msa_pdb_index,
            missing_res_dict,
            structure_count,
            network_index,
        )
    else:
        missing_contacts = {}
        missing_contacts_colors = {}
        missing_contacts_properties = pd.DataFrame()
    return (
        conservation_tem_msa_dr,
        colors_int_type,
        properties,
        missing_contacts,
        missing_contacts_colors,
        missing_contacts_properties,
    )


def conservation_nextwork_dict(
    all_int_dict: dict,
    missing_res_dict: dict,
    target_msa_pdb_dict: dict,
    target_structure: str,
    index_type: str,
    conservation_uniform=True,
) -> tuple[dict, dict, pd.DataFrame]:
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
    common_int_type_list = []
    common_loc_list = []
    Res1_msa_list = []
    Res2_msa_list = []
    Res1_pdb_list = []
    Res2_pdb_list = []
    structure_int_type_list = []
    structure_loc_list = []
    conservation_list = []

    for target_contacts, target_properties in target_contacts_dict.items():
        contact_yes = 0
        contact_no = 0
        contact_dna = 0
        total_structure = 0
        target_res1 = target_contacts[0]
        target_res2 = target_contacts[1]
        target_int_type = target_properties[0]
        contact_int_type_list = []
        contact_loc_list = []

        for structure, contact_dict in all_int_dict.items():
            if structure != target_structure:
                total_structure += 1
                missing_res_list = missing_res_dict[structure]
                if target_res1 in missing_res_list or target_res2 in missing_res_list:
                    contact_dna += 1
                    continue

                if (target_res1, target_res2) in contact_dict:
                    properties = contact_dict[(target_res1, target_res2)]
                    contact_yes += 1
                    contact_int_type_list.append(properties[0])
                    contact_loc_list.append(properties[1])

                elif (
                    target_res2,
                    target_res1,
                ) in contact_dict:
                    properties = contact_dict[(target_res2, target_res1)]
                    contact_yes += 1
                    contact_int_type_list.append(properties[0])
                    contact_loc_list.append(properties[1])

                else:
                    contact_no += 1
        if len(contact_int_type_list) != 0 and len(contact_loc_list) != 0:
            contact_int_type_count = Counter(contact_int_type_list)
            contact_loc_count = Counter(contact_loc_list)
            common_int_type = contact_int_type_count.most_common(1)[0][0]
            common_loc = contact_loc_count.most_common(1)[0][0]
            common_int_type_list.append(common_int_type)
            common_loc_list.append(common_loc)
        else:
            common_int_type_list.append("None")
            common_loc_list.append("None")
        Res1_msa_list.append(target_res1)
        Res2_msa_list.append(target_res2)
        structure_int_type_list.append(target_int_type)
        structure_loc_list.append(target_properties[1])
        contact_pdb = target_msa_pdb_dict[(target_res1, target_res2)]
        contact_pdb = (int(contact_pdb[0][3:]), int(contact_pdb[1][3:]))
        Res1_pdb_list.append(contact_pdb[0])
        Res2_pdb_list.append(contact_pdb[1])
        if conservation_uniform == True:
            conservation[(target_res1, target_res2)] = contact_yes / (
                contact_dna + contact_no + contact_yes
            )
        else:
            conservation[(target_res1, target_res2)] = contact_yes / (
                contact_no + contact_yes
            )
        conservation_list.append(conservation[(target_res1, target_res2)])

        conservation_int_type[(target_res1, target_res2)] = colors[target_int_type]
    if index_type == "msa":
        dir_out = conservation
        colors_int_type = conservation_int_type
        properties_df = pd.DataFrame(
            {
                "Res1_msa": Res1_msa_list,
                "Res2_msa": Res2_msa_list,
                "Res1_pdb": Res1_pdb_list,
                "Res2_pdb": Res2_pdb_list,
                "Int_Type": structure_int_type_list,
                "Location": structure_loc_list,
                "Conservation": conservation_list,
                "Common_Int_Type": common_int_type_list,
                "Common_Loc": common_loc_list,
            }
        )

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
        properties_df = pd.DataFrame(
            {
                "Res1_msa": Res1_msa_list,
                "Res2_msa": Res2_msa_list,
                "Res1_pdb": Res1_pdb_list,
                "Res2_pdb": Res2_pdb_list,
                "Int_Type": structure_int_type_list,
                "Conservation": conservation_list,
                "Location": structure_loc_list,
                "Common_Int_Type": common_int_type_list,
                "Common_Loc": common_loc_list,
            }
        )

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
        quit()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Function: conservation_nextwork_dict")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
    return dir_out, colors_int_type, properties_df


def conservation_nextwork_df(
    all_int_df: dict,
    target_msa_pdb_dict: dict,
    target_structure: str,
    index_type: str,
    conservation_uniform=True,
    exclude_vdw=True,
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
        if conservation_uniform == True:
            conservation[(target_res1_msa, target_res2_msa)] = contact_yes / (
                contact_dna + contact_no + contact_yes
            )
        else:
            conservation[(target_res1_msa, target_res2_msa)] = contact_yes / (
                contact_no + contact_yes
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


def missing_contacts_dict(
    all_interactions_dict: dict,
    target_structure: str,
    target_msa_pdb_dict: dict,
    missing_res_dict: dict,
    structure_count: int,
    network_index="pdb",
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
            "Res1_msa",
            "Res2_pdb",
            "Res1_pdb",
            "Res2_pdb",
            "conservation",
            "Int_Type",
            "Int_Type_Percent",
            "Location",
            "Location_percent",
        )
    )
    missing_contacts = {}
    missing_contacts_colors = {}
    target_contacts_dict = all_interactions_dict[target_structure]
    missing_residues = []
    for msa, pdb in target_msa_pdb_dict.items():
        if pdb == None:
            missing_residues.append(msa)
    for structure, contact_dict in all_interactions_dict.items():
        if structure != target_structure:
            for contact, _ in contact_dict.items():
                if (contact[0], contact[1]) not in target_contacts_dict and (
                    contact[1],
                    contact[0],
                ) not in target_contacts_dict:
                    if contact[0] in missing_residues or contact[1] in missing_residues:
                        continue
                    if contact not in missing_contacts_count:
                        missing_contacts_count[contact] = 1
                    else:
                        missing_contacts_count[contact] += 1
    counter = 0
    int_type_list = []
    int_type_count_list = []
    location_list = []
    location_count_list = []
    res1_pdb = []
    res2_pdb = []
    res1_msa = []
    res2_msa = []
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

        counter += 1
        contact_pdb_1 = target_msa_pdb_dict[contact[0]]
        contact_pdb_2 = target_msa_pdb_dict[contact[1]]
        if contact_pdb_1 == None or contact_pdb_2 == None:
            print("ERROR, MISSING INTERACTION OCCURS AT THE MISSING RESIDUE")
            return None
        contact_pdb = (contact_pdb_1, contact_pdb_2)
        res1_msa.append(contact[0])
        res2_msa.append(contact[1])
        res1_pdb.append(contact_pdb[0])
        res2_pdb.append(contact_pdb[1])

        if network_index == "pdb":
            missing_contacts[contact_pdb] = value / structure_count
            missing_contacts_colors[contact_pdb] = colors[common_int_type]
        else:
            missing_contacts[contact] = value / structure_count
            missing_contacts_colors[contact] = colors[common_int_type]

        int_type_list.append(common_int_type)
        int_type_count_list.append(100 * (count_int_type / len(int_type)))
        location_list.append(common_location)
        location_count_list.append(100 * (count_location / len(location)))

    missing_contacts_properties["Res1_msa"] = res1_msa
    missing_contacts_properties["Res2_msa"] = res2_msa
    missing_contacts_properties["Res1_pdb"] = res1_pdb
    missing_contacts_properties["Res2_pdb"] = res2_pdb
    missing_contacts_properties["Concervation"] = missing_contacts.values()
    missing_contacts_properties["Int_Type"] = int_type_list
    missing_contacts_properties["Int_Percent"] = int_type_count_list
    missing_contacts_properties["Location"] = location_list
    missing_contacts_properties["Location_Percent"] = location_count_list
    print("Number of missing contacts:", len(missing_contacts))
    return missing_contacts, missing_contacts_colors, missing_contacts_properties


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


def filter_network(
    network,
    colors,
    properties,
    min_score=0.0,
    network_index="pdb",
    loc_exclude=None,
    int_exclude=None,
):
    new_network = {}
    new_network_colors = {}
    combined_mask = pd.Series(False, index=properties.index)
    for key, value in network.items():
        if network_index == "pdb":
            mask_1 = (properties["Res1_pdb"] == key[0]) & (
                properties["Res2_pdb"] == key[1]
            )
            mask_2 = (properties["Res1_pdb"] == key[1]) & (
                properties["Res2_pdb"] == key[0]
            )
        elif network_index == "msa":
            mask_1 = (properties["Res1_msa"] == key[0]) & (
                properties["Res2_msa"] == key[1]
            )
            mask_2 = (properties["Res1_msa"] == key[1]) & (
                properties["Res2_msa"] == key[0]
            )
        else:
            print("ERROR: Incorrect indexing type is specified for the network")
            print("-----------------------------------------------------------")
            return None, None, None
        mask_12 = mask_1 | mask_2
        if value > min_score:
            if loc_exclude is not None:
                location = properties.loc[mask_12, "Location"]
                if len(location) == 1:
                    if location.item() in loc_exclude:
                        continue
                elif len(location) != 0:
                    print(location)
                    print(len(location))
            # location_1 = properties.loc[mask_1, "Location"]
            # location_2 = properties.loc[mask_2, "Location"]
            # locs = [location_1, location_2]
            # for loc in locs:
            #     if len(loc) == 1:
            #         if loc.item() in loc_exclude:
            #             continue
            if int_exclude is not None:
                for interaction in int_exclude:
                    if (
                        interaction in properties.loc[mask_1, "Int_Type"].values
                        or interaction in properties.loc[mask_2, "Int_Type"].values
                    ):
                        continue
            new_network[key] = value
            new_network_colors[key] = colors[key]
            combined_mask = combined_mask | mask_12
    new_properties = properties[combined_mask]
    return new_network, new_network_colors, new_properties


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


def plot_int_map(grid, title, color="Reds", threshold=0.1):
    x_coords, y_coords = np.meshgrid(np.arange(grid.shape[0]), np.arange(grid.shape[1]))
    x_coords = x_coords.flatten()
    y_coords = y_coords.flatten()
    plt.rcParams["font.size"] = 20
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
    cmap = plt.cm.get_cmap(color)
    normalize = plt.Normalize(0.1, 1)
    scatter = ax.scatter(
        x_coords, y_coords, c=values, cmap=cmap, norm=normalize, marker="s", s=10
    )

    cbar = plt.colorbar(scatter)
    cbar.set_label("Conservation Score")

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


def get_per_res_score(
    conservation_dict,
):
    per_res_score_dict = {}
    for key, value in conservation_dict.items():
        if key[0] in per_res_score_dict.keys():
            per_res_score_dict[key[0]] += value
        else:
            per_res_score_dict[key[0]] = value
        if key[1] in per_res_score_dict.keys():
            per_res_score_dict[key[1]] += value
        else:
            per_res_score_dict[key[1]] = value
    max_score = max(per_res_score_dict.values())
    min_score = min(per_res_score_dict.values())
    for key, value in per_res_score_dict.items():
        per_res_score_dict[key] = (per_res_score_dict[key] - min_score) / (
            max_score - min_score
        )
    return per_res_score_dict


def plot_per_res_score(
    residue_score_dict,
    max_residue,
    important_residues,
    close_residues,
    title,
    bar=False,
):
    """
    Plots per-residue scores.

    Parameters:
    - residue_score_dict: A dictionary where the key is residue number and value is the score.
    - important_residues: A list of residue indices that are experimentally important and should be highlighted.
    - close_residues: residues within the active site (within 5 angstroms of the ligand)
    - max_residue: The maximum residue number you're interested in (defines the range for x-axis).
    - title: The title of the plot.
    Returns:
    - A plot of the scores with important residues highlighted.
    """

    # Create a list of residue indices
    scored_residues = [
        residue for residue in residue_score_dict.keys() if residue <= max_residue
    ]
    scores = [residue_score_dict[residue] for residue in scored_residues]
    #    if bar == True:
    print(close_residues)
    print(important_residues)
    colors = [
        "lime"
        if residue in important_residues
        else "magenta"
        if residue in close_residues
        else "grey"
        for residue in scored_residues
    ]
    overlap = []
    for res in scored_residues:
        if res in close_residues:
            overlap.append(res)
    print("Overlap", overlap)

    value_color = list(zip(scores, colors, scored_residues))
    sorted_zipped = sorted(value_color, key=lambda x: x[0], reverse=True)
    sorted_values, sorted_colors, sorted_residues = zip(*sorted_zipped)
    no_0_list = list(filter(lambda x: x != 0, sorted_values))
    sorted_colors = sorted_colors[: len(no_0_list)]
    plt.bar(
        range(len(sorted_colors)), no_0_list, color=sorted_colors
    )  # s=50 to increase size of scatter points
    # plt.xticks(fontsize=18)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.xlabel("Hierarchical Residue Index", fontsize=20)
    plt.ylabel("KIN per Residue Conservation", fontsize=20)
    # plt.title(f"{title}", fontsize=20)

    # Set x-axis limits to display entire residue range
    plt.xlim(-3, len(sorted_colors) + 1)

    # Highlight important residues in the legend
    plt.legend(
        handles=[
            plt.Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                markerfacecolor="magenta",
                markersize=10,
                label="Active Site",
            ),
            plt.Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                markerfacecolor="lime",
                markersize=10,
                label="Catalytic Residue",
            ),
            plt.Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                markerfacecolor="grey",
                markersize=10,
                label="Other",
            ),
        ],
        loc="upper right",
        fontsize=18,
        edgecolor="black",
    )

    # plt.show()

    # Sort the scores and get the indices
    # sorted_indices = np.argsort(scores)[::-1]
    # print(sorted_indices)
    # Initialize counters for true positive and false positive
    true_pos_imp = 0
    true_pos_close = 0
    # Initialize lists to store fractions
    fractions_imp = []
    fractions_close = []
    print("important residues", important_residues)
    # Iterate over different top percentages
    for percentage in range(10, 101, 10):
        top_n = int(len(scores) * percentage / 100)
        top_indices = sorted_residues[:top_n]
        print(top_indices)
        # Count how many important residues are in the top
        true_pos_imp = len(set(top_indices) & set(important_residues))
        true_pos_close = len(set(top_indices) & set(close_residues))
        print("true positive:", true_pos_close)
        print("true positive:", true_pos_imp)
        # Compute the fraction of total important residues identified
        fraction_imp = true_pos_imp / len(important_residues)
        fraction_close = true_pos_close / len(close_residues)
        fractions_imp.append(fraction_imp)
        fractions_close.append(fraction_close)
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.ylim(0, 1.1)
    plt.plot(
        range(10, 101, 10),
        fractions_imp,
        marker="o",
        color="limegreen",
        linewidth=2,
        label=f"Catalytic Residues (n={len(important_residues)})",
    )
    plt.plot(
        range(10, 101, 10),
        fractions_close,
        marker="x",
        color="magenta",
        linewidth=2,
        label=f"Active Site (n={len(close_residues)})",
    )
    plt.xlabel("Top Percentage of all Ranked Residues", fontsize=20)
    plt.ylabel("Fraction of Important Residues Scored", fontsize=20)
    plt.yticks(fontsize=18)
    plt.xticks(fontsize=18)
    plt.legend(fontsize=20, edgecolor="black")
    plt.grid(True)
    plt.show()
