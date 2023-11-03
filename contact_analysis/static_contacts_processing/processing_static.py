from fileinput import filename
from tkinter import W, font
from matplotlib import colors
from scipy.stats import pearsonr
from kin.pymol_projections import project_pymol_res_res_scores
import pandas as pd
import kin.msa_network as toolsnet
import matplotlib.pyplot as plt
import numpy as np
import json
import seaborn as sns

# network_crystal_file = "static_contacts_processing/shared_network/network_tem1_pdb.csv"
network_crystal_file_sc = "shared_network/network_tem1_sc_nvd_pdb.csv"
network_crystal_file_nvd = "shared_network/network_tem1_nvd_pdb.csv"
colors_sc = "colors_tem1_sc_nvd_pdb.csv"
colors_nvd = "colors_tem1_nvd_pdb.csv"
miss_network = "miss_tem1_sc_nvd_pdb.csv"
miss_colors = "miss_colors_tem1_sc_nvd_pdb.csv"
miss_props = pd.read_csv("miss_prop_tem1_sc_nvd_pdb.csv")
network_crystal_sc = toolsnet.get_contacts_from_csv(network_crystal_file_sc)
network_crystal = toolsnet.get_contacts_from_csv(network_crystal_file_nvd)
colors_sc_dic = toolsnet.get_contacts_from_csv(colors_sc, value_type="str")
colors_nvd_dic = toolsnet.get_contacts_from_csv(colors_nvd, value_type="str")
miss_network_crystal = toolsnet.get_contacts_from_csv(miss_network)
miss_colors_sc_dic = toolsnet.get_contacts_from_csv(miss_colors, value_type="str")
print(miss_props)
above_05_net = {}
above_05_colors = {}
only_hydrophobic = {}
only_hydrophobic_colors = {}
conserved_90 = {}
conserved_90_colors = {}
for key, value in network_crystal.items():
    if colors_nvd_dic[key] == "br9":
        only_hydrophobic[key] = value
        only_hydrophobic_colors[key] = colors_nvd_dic[key]
    if value >= 0.9:
        conserved_90[key] = value
        conserved_90_colors[key] = colors_nvd_dic[key]
project_pymol_res_res_scores(
    only_hydrophobic, "hydrophobic_nvd_network.pml", only_hydrophobic_colors
)
project_pymol_res_res_scores(
    conserved_90, "above_90_nvd_network.pml", conserved_90_colors
)


for key, value in miss_network_crystal.items():
    if value >= 0.5:
        above_05_net[key] = value
        above_05_colors[key] = miss_colors_sc_dic[key]
        print(miss_props[miss_props["Contact"] == f"{key}"])
project_pymol_res_res_scores(
    above_05_net, "miss_05_nvd_sc_network.pml", above_05_colors
)
# print items of the miss_props dataframe where Contact in the same as the key in above_05_net
filtered_df = miss_props[miss_props["Contact"].isin(above_05_net.keys())]
# Print the filtered DataFrame
print(filtered_df)
print(miss_props[miss_props["Contact"] == "(145, 214)"])

# per res score conmpared to fitness scores
fitness_data = "per_res_fitness_scores.json"

with open(fitness_data) as f:
    fitness_scores_dict = json.load(f)
res_names = []
res_scores = []
for keys in above_05_net.keys():
    if str(keys[0]) in fitness_scores_dict.keys():
        res_names.append(keys[0])
        res_scores.append(fitness_scores_dict[str(keys[0])])
        removed_res = fitness_scores_dict.pop(str(keys[0]))

    if str(keys[1]) in fitness_scores_dict.keys():
        res_names.append(keys[1])
        res_scores.append(fitness_scores_dict[str(keys[1])])
        removed_res = fitness_scores_dict.pop(str(keys[1]))
fitness_res = []
fitness_scores = []
for key in fitness_scores_dict.keys():
    fitness_res.append(int(key))
    fitness_scores.append(fitness_scores_dict[key])
print(res_names)
print(res_scores)
fig, ax = plt.subplots()
ax.scatter(
    res_scores, res_names, color="r", label="Contacts with conservation score > 0.5"
)
ax.scatter(fitness_scores, fitness_res, color="b", label="Fitness Scores")
ax.set_xlabel("Conservation Score", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
ax.set_ylabel("Residue Number", fontsize=14)
ax.legend()
plt.title("Conservation Score vs Residue Number", fontsize=18)
plt.show()

network_crystal_list = []
network_crystal_sc_list = []
for key in network_crystal:
    network_crystal_list.append(network_crystal[key])
for key in network_crystal_sc:
    network_crystal_sc_list.append(network_crystal_sc[key])
fig, ax1 = plt.subplots()
# Create the first histogram on the primary axis
plt.grid(axis="y", linestyle="--", alpha=0.5)
ax1.hist(
    network_crystal_list,
    bins=10,
    alpha=0.5,
    color="blue",
    edgecolor="black",
    label="All Contacts",
)
ax1.set_xlabel("Conservation Score", fontsize=20, color="black")
ax1.set_ylabel("Number of Contacts", color="black", fontsize=20)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

ax1.tick_params(axis="y", labelcolor="black")
# Create the second histogram on the secondary axis
ax1.hist(
    network_crystal_sc_list,
    bins=10,
    color="salmon",
    edgecolor="black",
    label="Side Chain Contacts",
)

# Add a legend for both histograms
lines, labels = ax1.get_legend_handles_labels()
ax1.legend(lines, labels, loc="upper left", fontsize=20)

# Set the title
plt.title("Contact Distribution for TEM-1", fontsize=22)

# Show the plot
plt.tight_layout()
plt.show()
fig, ax = plt.subplots()
# sns.kdeplot(network_crystal_list, label="All Contacts", color="blue", ax=ax)
# sns.kdeplot(network_crystal_sc_list, label="Side Chain Contacts", color="red", ax=ax)
sns.histplot(
    network_crystal_list,
    bins=15,
    kde=True,
    color="blue",
    label="Distribution 1",
    common_norm=True,
    element="step",
    fill=True,
    ax=ax,
)
sns.histplot(
    network_crystal_sc_list,
    bins=15,
    kde=True,
    color="red",
    label="Distribution 2",
    common_norm=True,
    element="step",
    fill=True,
    ax=ax,
)

# Set labels and title
ax.set_xlabel("Conservation Score")
ax.set_ylabel("Number of Contacts")
plt.title("Comparison of Contact Distributions for TEM-1")

# Add a legend
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()
