from math import e
from tkinter import font
from scipy.stats import pearsonr
import numpy as np
import matplotlib.pyplot as plt
import csv
import ast
from tools_proj.pymol_projections import project_pymol_res_res_scores
from collections import Counter

total_res_number = 263
network_crystal_file = "static_contacts_processing/shared_network/network_tem1_nvw_pdb.csv"
colors_crystal_file = "static_contacts_processing/shared_network/colors_tem1_nvw_pdb.csv"
network_md_file_50 = (
    "dynamic_contacts_processing/shared_network/network_tem1_pdb_nv_50.csv"
)
colors_md_file_50 = (
    "dynamic_contacts_processing/shared_network/colors_tem1_pdb_nv_50.csv"
)
network_md_file_10 = (
    "dynamic_contacts_processing/shared_network/network_tem1_pdb_nv_10.csv"
)
colors_md_file_10 = (
    "dynamic_contacts_processing/shared_network/colors_tem1_pdb_nv_10.csv"
)


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
    print("Total Number of Contacts in the Difference Network:", len(diff_network))
    print("Number of Only MD Contacts:", counter_only_md)
    print("Number of Only Crystal Contacts:", counter_only_crystal)
    return diff_network, diff_colors, diff_list


def plot_int_map(grid, title):
    threshold = 0.1

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


def plot_hist_of_contacts(contact, title, filename, color="blue"):
    if isinstance(contact, dict):
        contact_score_list = []
        for key, value in contact.items():
            contact_score_list.append(value)
    elif isinstance(contact, list):
        contact_score_list = contact
        identities = color
        if isinstance(color, list):
            bins = [0, 0.2, 0.4, 0.6, 0.8, 1]
            bin_data = {}
            for i in range(len(bins) - 1):
                bin_data[(bins[i], bins[i + 1])] = Counter()

            # Sort scores into bins and count interactions
            for score, identity in zip(contact_score_list, identities):
                for low, high in bin_data.keys():
                    if low <= score < high:
                        bin_data[(low, high)][identity] += 1
                        break

            # Calculate fractional compositions
            fraction_data = {}
            for bin_range, counts in bin_data.items():
                total = sum(counts.values())
                if total > 0:
                    fraction_data[bin_range] = {k: v / total for k, v in counts.items()}
            # Plotting
            fig, ax = plt.subplots()

            # X-axis positions for the bins
            x_pos = np.arange(len(bin_data.keys()))
            x_labels = [f"{low}-{high}" for low, high in bin_data.keys()]

            for i, (low, high) in enumerate(bin_data.keys()):
                bottom_value = 0
                for identity, fraction in fraction_data.get((low, high), {}).items():
                    ax.bar(
                        x_pos[i],
                        fraction,
                        width=0.4,
                        label=identity if i == 0 else "",
                        bottom=bottom_value,
                        edgecolor="black",
                    )
                    bottom_value += fraction
            # Labels and title
            ax.set_ylabel("Fraction of Interactions")
            ax.set_xlabel("Conservation Score Bins")
            ax.set_title("Fractional Composition of Interaction Types per Bin")
            ax.set_xticks(x_pos)
            ax.set_xticklabels(x_labels)
            ax.legend()

            plt.show()
            exit()
    else:
        raise TypeError("Contact must be either a list or a dictionary")

    plt.hist(contact_score_list, bins=10, alpha=0.7, color=color, edgecolor="black")

    plt.xlabel("Conservation Scores", fontsize=16)
    plt.ylabel("Number of Contacts", fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.title(title, fontsize=18)

    plt.grid(axis="y", linestyle="--", alpha=0.9)
    plt.savefig(filename)
    plt.show()


network_crystal = get_contacts_from_csv(network_crystal_file)
network_md_10 = get_contacts_from_csv(network_md_file_10)
network_md_50 = get_contacts_from_csv(network_md_file_50)
colors_crystal = get_contacts_from_csv(colors_crystal_file, value_type=str)
colors_md_10 = get_contacts_from_csv(colors_md_file_10, value_type=str)
colors_md_50 = get_contacts_from_csv(colors_md_file_50, value_type=str)

contacts_lost_from10_to50 = []
colors = []
for key, value in network_md_10.items():
    if key not in network_md_50:
        contacts_lost_from10_to50.append(value)
        colors.append(colors_md_10[key])

plot_hist_of_contacts(
    contacts_lost_from10_to50,
    "Contacts Lost from 10% to 50% MD Cutoff",
    "contacts_lost_from10_to50.png",
    color="mediumaquamarine",
)
high_score_counter = 0
for i in contacts_lost_from10_to50:
    if i > 0.8:
        high_score_counter += 1
print(
    "Number of Contacts with Score > 0.8:",
    high_score_counter / len(contacts_lost_from10_to50),
)
print(high_score_counter)
print(len(contacts_lost_from10_to50))
diff_network_50_0, diff_colors_50_0, diff_list_50_0 = difference_matrix(
    network_crystal,
    colors_crystal,
    network_md_50,
    colors_md_50,
    diff_threshold=0.0,
    only_overlap=True,
)
FILENAME_PYMOL = "tem1_only_overlap_contacts_50_0.pml"
# project_pymol_res_res_scores(diff_network_50_0, FILENAME_PYMOL, diff_colors_50_0)

diff_network_10_0, diff_colors_10_0, diff_list_10_0 = difference_matrix(
    network_crystal,
    colors_crystal,
    network_md_10,
    colors_md_10,
    diff_threshold=0.0,
    only_overlap=True,
)
FILENAME_PYMOL = "tem1_only_overlap_contacts_10_0.pml"
# project_pymol_res_res_scores(diff_network_10_0, FILENAME_PYMOL, diff_colors_10_0)

diff_network_50_02, diff_colors_50_02, diff_list_50_02 = difference_matrix(
    network_crystal,
    colors_crystal,
    network_md_50,
    colors_md_50,
    diff_threshold=0.2,
    only_overlap=True,
)
FILENAME_PYMOL = "tem1_only_overlap_contacts_50_02.pml"
# project_pymol_res_res_scores(diff_network_50_02, FILENAME_PYMOL, diff_colors_50_02)

diff_network_10_02, diff_colors_10_02, diff_list_10_02 = difference_matrix(
    network_crystal,
    colors_crystal,
    network_md_10,
    colors_md_10,
    diff_threshold=0.2,
    only_overlap=True,
)
FILENAME_PYMOL = "tem1_only_overlap_contacts_10_02.pml"
# project_pymol_res_res_scores(diff_network_10_02, FILENAME_PYMOL, diff_colors_10_02)

diff_network_50_05, diff_colors_50_05, diff_list_50_05 = difference_matrix(
    network_crystal,
    colors_crystal,
    network_md_50,
    colors_md_50,
    diff_threshold=0.5,
)
diff_network_10_05, diff_colors_10_05, diff_list_10_05 = difference_matrix(
    network_crystal,
    colors_crystal,
    network_md_10,
    colors_md_10,
    diff_threshold=0.5,
)
diff_network_50_07, diff_colors_50_07, diff_list_50_07 = difference_matrix(
    network_crystal,
    colors_crystal,
    network_md_50,
    colors_md_50,
    diff_threshold=0.7,
)
diff_network_10_07, diff_colors_10_07, diff_list_10_07 = difference_matrix(
    network_crystal,
    colors_crystal,
    network_md_10,
    colors_md_10,
    diff_threshold=0.7,
)
grid_from_difference_10_0 = make_grid(diff_network_10_0, total_res_number)
grid_from_difference_50_0 = make_grid(diff_network_50_0, total_res_number)
grid_from_difference_10_02 = make_grid(diff_network_10_02, total_res_number)
grid_from_difference_50_02 = make_grid(diff_network_50_02, total_res_number)
grid_from_difference_50_05 = make_grid(diff_network_50_05, total_res_number)
grid_from_difference_10_05 = make_grid(diff_network_10_05, total_res_number)
grid_from_difference_50_07 = make_grid(diff_network_50_07, total_res_number)
grid_from_difference_10_07 = make_grid(diff_network_10_07, total_res_number)
corr_coef_05, _ = pearsonr(
    grid_from_difference_10_05.flatten(), grid_from_difference_10_0.flatten()
)
corr_coef_0, _ = pearsonr(
    grid_from_difference_10_0.flatten(), grid_from_difference_50_0.flatten()
)
corr_coef_02, _ = pearsonr(
    grid_from_difference_10_02.flatten(), grid_from_difference_50_02.flatten()
)
corr_coef_50_07, _ = pearsonr(
    grid_from_difference_50_0.flatten(), grid_from_difference_50_07.flatten()
)
corr_coef_10_07, _ = pearsonr(
    grid_from_difference_10_0.flatten(), grid_from_difference_10_07.flatten()
)
corr_coef_10, _ = pearsonr(
    grid_from_difference_10_0.flatten(), grid_from_difference_10_02.flatten()
)
corr_coef_50, _ = pearsonr(
    grid_from_difference_50_0.flatten(), grid_from_difference_50_02.flatten()
)
print("Correlation coefficient at 50% MD filtering:", corr_coef_50)
print("Correlation coefficient at 10% MD filtering:", corr_coef_10)
print("Correlation coefficient at 10% MD filtering and 0.7 break:", corr_coef_10_07)
print("Correlation coefficient at 50% MD filtering and 0.7 break:", corr_coef_50_07)
print("Correlation coefficient with 0 threshold:", corr_coef_0)
print("Correlation coefficient with 0.2 threshold:", corr_coef_02)
print("Correlation coefficient with 0.5 threshold:", corr_coef_05)
plot_int_map(grid_from_difference_50_0, "50% MD filtering and 0.7 break")
plot_int_map(grid_from_difference_10_0, "10% MD filtering and 0.7 break")
