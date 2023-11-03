from fileinput import filename
from tkinter import W, font
from scipy.stats import pearsonr
from kin.pymol_projections import project_pymol_res_res_scores
import pandas as pd
import kin.msa_network as toolsnet
import matplotlib.pyplot as plt
import numpy as np


network_crystal_file = (
    "static_contacts_processing/shared_network/network_tem1_nvw_pdb.csv"
)
# network_crystal_file = "static_contacts_processing/shared_network/network_tem1_pdb.csv"
colors_crystal_file = (
    "static_contacts_processing/shared_network/colors_tem1_nvw_pdb.csv"
)
# ________________________________________

network_md_file_95 = (
    "dynamic_contacts_processing/shared_network/network_tem1_pdb_nvw_95.csv"
)
network_md_file_90 = (
    "dynamic_contacts_processing/shared_network/network_tem1_pdb_nvw_90.csv"
)
network_md_file_80 = (
    "dynamic_contacts_processing/shared_network/network_tem1_pdb_nvw_80.csv"
)
network_md_file_70 = (
    "dynamic_contacts_processing/shared_network/network_tem1_pdb_nvw_70.csv"
)
network_md_file_60 = (
    "dynamic_contacts_processing/shared_network/network_tem1_pdb_nvw_60.csv"
)
network_md_file_50 = (
    "dynamic_contacts_processing/shared_network/network_tem1_pdb_nvw_50.csv"
)
network_md_file_40 = (
    "dynamic_contacts_processing/shared_network/network_tem1_pdb_nvw_40.csv"
)
network_md_file_30 = (
    "dynamic_contacts_processing/shared_network/network_tem1_pdb_nvw_30.csv"
)
network_md_file_20 = (
    "dynamic_contacts_processing/shared_network/network_tem1_pdb_nvw_20.csv"
)
network_md_file_10 = (
    "dynamic_contacts_processing/shared_network/network_tem1_pdb_nvw_10.csv"
)
network_md_file_0 = (
    "dynamic_contacts_processing/shared_network/network_tem1_pdb_nvw_0.csv"
)
# ________________________________________

colors_md_file_95 = (
    "dynamic_contacts_processing/shared_network/colors_tem1_pdb_nvw_95.csv"
)
colors_md_file_90 = (
    "dynamic_contacts_processing/shared_network/colors_tem1_pdb_nvw_90.csv"
)
colors_md_file_80 = (
    "dynamic_contacts_processing/shared_network/colors_tem1_pdb_nvw_80.csv"
)
colors_md_file_70 = (
    "dynamic_contacts_processing/shared_network/colors_tem1_pdb_nvw_70.csv"
)
colors_md_file_60 = (
    "dynamic_contacts_processing/shared_network/colors_tem1_pdb_nvw_60.csv"
)
colors_md_file_50 = (
    "dynamic_contacts_processing/shared_network/colors_tem1_pdb_nvw_50.csv"
)
colors_md_file_40 = (
    "dynamic_contacts_processing/shared_network/colors_tem1_pdb_nvw_40.csv"
)
colors_md_file_30 = (
    "dynamic_contacts_processing/shared_network/colors_tem1_pdb_nvw_30.csv"
)
colors_md_file_20 = (
    "dynamic_contacts_processing/shared_network/colors_tem1_pdb_nvw_20.csv"
)
colors_md_file_10 = (
    "dynamic_contacts_processing/shared_network/colors_tem1_pdb_nvw_10.csv"
)
colors_md_file_0 = (
    "dynamic_contacts_processing/shared_network/colors_tem1_pdb_nvw_0.csv"
)

TOTAL_RES_NUMBER = 263

network_crystal = toolsnet.get_contacts_from_csv(network_crystal_file)
network_md_0 = toolsnet.get_contacts_from_csv(network_md_file_0)
network_md_10 = toolsnet.get_contacts_from_csv(network_md_file_10)
network_md_20 = toolsnet.get_contacts_from_csv(network_md_file_20)
network_md_30 = toolsnet.get_contacts_from_csv(network_md_file_30)
network_md_40 = toolsnet.get_contacts_from_csv(network_md_file_40)
network_md_50 = toolsnet.get_contacts_from_csv(network_md_file_50)
network_md_60 = toolsnet.get_contacts_from_csv(network_md_file_60)
network_md_70 = toolsnet.get_contacts_from_csv(network_md_file_70)
network_md_80 = toolsnet.get_contacts_from_csv(network_md_file_80)
network_md_90 = toolsnet.get_contacts_from_csv(network_md_file_90)
network_md_95 = toolsnet.get_contacts_from_csv(network_md_file_95)

colors_crystal = toolsnet.get_contacts_from_csv(colors_crystal_file, value_type=str)
colors_md_0 = toolsnet.get_contacts_from_csv(colors_md_file_0, value_type=str)
colors_md_10 = toolsnet.get_contacts_from_csv(colors_md_file_10, value_type=str)
colors_md_20 = toolsnet.get_contacts_from_csv(colors_md_file_20, value_type=str)
colors_md_30 = toolsnet.get_contacts_from_csv(colors_md_file_30, value_type=str)
colors_md_40 = toolsnet.get_contacts_from_csv(colors_md_file_40, value_type=str)
colors_md_50 = toolsnet.get_contacts_from_csv(colors_md_file_50, value_type=str)
colors_md_60 = toolsnet.get_contacts_from_csv(colors_md_file_60, value_type=str)
colors_md_70 = toolsnet.get_contacts_from_csv(colors_md_file_70, value_type=str)
colors_md_80 = toolsnet.get_contacts_from_csv(colors_md_file_80, value_type=str)
colors_md_90 = toolsnet.get_contacts_from_csv(colors_md_file_90, value_type=str)
colors_md_95 = toolsnet.get_contacts_from_csv(colors_md_file_95, value_type=str)


colors_list = [
    colors_md_0,
    colors_md_10,
    colors_md_20,
    colors_md_30,
    colors_md_40,
    colors_md_50,
    colors_md_60,
    colors_md_70,
    colors_md_80,
    colors_md_90,
    colors_md_95,
]
nets_list = [
    network_md_0,
    network_md_10,
    network_md_20,
    network_md_30,
    network_md_40,
    network_md_50,
    network_md_60,
    network_md_70,
    network_md_80,
    network_md_90,
    network_md_95,
]
shared_count = []
net_len_list = []
shared_count_no_norm = []
hbond_list = []
vdw_list = []
saltbridge_list = []
hydrophobic_list = []
pipi_list = []
cationpi_list = []

for index, md_net in enumerate(nets_list):
    hbond = 0
    vdw = 0
    saltbridge = 0
    hydrophobic = 0
    pipi = 0
    cationpi = 0
    count = 0
    net_len_list.append(len(md_net))
    for key, value in md_net.items():
        if colors_list[index][key] == "br1":
            hbond += 1
        if colors_list[index][key] == "green":
            vdw += 1
        if colors_list[index][key] == "dash":
            saltbridge += 1
        if colors_list[index][key] == "br9":
            hydrophobic += 1
        if colors_list[index][key] == "br5":
            pipi += 1
        if colors_list[index][key] == "brightorange":
            cationpi += 1
    for key, value in network_crystal.items():
        if key in md_net:
            count += 1
    shared_count.append(count / len(network_crystal))
    shared_count_no_norm.append(count)
    hbond_list.append(hbond)
    vdw_list.append(vdw)
    saltbridge_list.append(saltbridge)
    hydrophobic_list.append(hydrophobic)
    pipi_list.append(pipi)
    cationpi_list.append(cationpi)

# Contact maps by interaction type for MD 10% cutoff and crystal structure
hbond_crystal = {}
hydrophobic_crystal = {}
other_crystal = {}
hbond_20md = {}
hydrophobic_20md = {}
other_20md = {}
for key, value in network_md_20.items():
    if colors_md_20[key] == "br1":
        hbond_20md[key] = value
    if colors_md_20[key] == "dash":
        other_20md[key] = value
    if colors_md_20[key] == "br9":
        hydrophobic_20md[key] = value
    if colors_md_20[key] == "br5":
        other_20md[key] = value
    if colors_md_20[key] == "brightorange":
        other_20md[key] = value
print("len of md 20:", len(network_md_20))
hbond_10md = {}
hydrophobic_10md = {}
other_10md = {}
for key, value in network_md_10.items():
    if colors_md_10[key] == "br1":
        hbond_10md[key] = value
    if colors_md_10[key] == "dash":
        other_10md[key] = value
    if colors_md_10[key] == "br9":
        hydrophobic_10md[key] = value
    if colors_md_10[key] == "br5":
        other_10md[key] = value
    if colors_md_10[key] == "brightorange":
        other_10md[key] = value
print("len of md 10:", len(network_md_10))
for key, value in network_crystal.items():
    if colors_crystal[key] == "br1":
        hbond_crystal[key] = value
    if colors_crystal[key] == "dash":
        other_crystal[key] = value
    if colors_crystal[key] == "br9":
        hydrophobic_crystal[key] = value
    if colors_crystal[key] == "br5":
        other_crystal[key] = value
    if colors_crystal[key] == "brightorange":
        other_crystal[key] = value
print("len of cs:", len(network_crystal))


grid_crystal = toolsnet.make_grid(network_crystal, TOTAL_RES_NUMBER)
grid_md_10 = toolsnet.make_grid(network_md_10, TOTAL_RES_NUMBER)
grid_md_20 = toolsnet.make_grid(network_md_20, TOTAL_RES_NUMBER)
grid_crystal_hbond = toolsnet.make_grid(hbond_crystal, TOTAL_RES_NUMBER)
grid_crystal_hydrophobic = toolsnet.make_grid(hydrophobic_crystal, TOTAL_RES_NUMBER)
grid_crystal_other = toolsnet.make_grid(other_crystal, TOTAL_RES_NUMBER)
grid_md_10_hbond = toolsnet.make_grid(hbond_10md, TOTAL_RES_NUMBER)
grid_md_10_hydrophobic = toolsnet.make_grid(hydrophobic_10md, TOTAL_RES_NUMBER)
grid_md_10_other = toolsnet.make_grid(other_10md, TOTAL_RES_NUMBER)
grid_md_20_hbond = toolsnet.make_grid(hbond_20md, TOTAL_RES_NUMBER)
grid_md_20_hydrophobic = toolsnet.make_grid(hydrophobic_20md, TOTAL_RES_NUMBER)
grid_md_20_other = toolsnet.make_grid(other_20md, TOTAL_RES_NUMBER)
corr_coef_10_20, _ = pearsonr(grid_md_10.flatten(), grid_md_20.flatten())
print("Correlation coefficient for 10 and 20% frames: ", corr_coef_10_20)
corr_coef_10, _ = pearsonr(grid_crystal.flatten(), grid_md_10.flatten())
corr_coef_20, _ = pearsonr(grid_crystal.flatten(), grid_md_20.flatten())
print("Correlation coefficient for 10% frames and crystal: ", corr_coef_10)
print("Correlation coefficient for 20% frames and crystal: ", corr_coef_20)
toolsnet.plot_int_map(
    grid_crystal_hbond, "H-bond Contacts from Crystal Structures", "Blues"
)
toolsnet.plot_int_map(
    grid_crystal_hydrophobic, "Hydrophobic Contacts from Crystal Structures", "Reds"
)
toolsnet.plot_int_map(
    grid_crystal_other, "Other Contacts from Crystal Structures", "Greens"
)
toolsnet.plot_int_map(grid_md_10_hbond, "H-bond Contacts from MD Simulations", "Blues")
toolsnet.plot_int_map(
    grid_md_10_hydrophobic, "Hydrophobic Contacts from MD Simulations", "Reds"
)
toolsnet.plot_int_map(grid_md_10_other, "Other Contacts from MD Simulations", "Greens")
# quit()
hbond = 0
vdw = 0
saltbridge = 0
hydrophobic = 0
pipi = 0
cationpi = 0
count = 0
for key, value in network_crystal.items():
    if colors_crystal[key] == "br1":
        hbond += 1
    if colors_crystal[key] == "green":
        vdw += 1
    if colors_crystal[key] == "dash":
        saltbridge += 1
    if colors_crystal[key] == "br9":
        hydrophobic += 1
    if colors_crystal[key] == "br5":
        pipi += 1
    if colors_crystal[key] == "brightorange":
        cationpi += 1
hbond_list.append(hbond)
vdw_list.append(vdw)
saltbridge_list.append(saltbridge)
hydrophobic_list.append(hydrophobic)
pipi_list.append(pipi)
cationpi_list.append(cationpi)

print(net_len_list)
print(len(network_crystal))

# make a bar graph where x axis is the number of frames and y axis is the number of contacts
# where the contacts are colored by the type of interaction

fig, ax1 = plt.subplots()
labels = ["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "95", "crystal"]

width = 0.6  # width of the bars
ind = np.arange(len(labels))  # the label locations
p2 = plt.bar(ind, hydrophobic_list, width, label="Hydrophobic", color="firebrick")

p4 = plt.bar(
    ind,
    hbond_list,
    width,
    bottom=np.array(hydrophobic_list),
    label="H-bond",
    color="royalblue",
)
p5 = plt.bar(
    ind,
    saltbridge_list,
    width,
    bottom=np.array(hydrophobic_list) + np.array(hbond_list),
    label="Salt bridge",
    color="gold",
)
p3 = plt.bar(
    ind,
    pipi_list,
    width,
    bottom=np.array(hydrophobic_list)
    + np.array(hbond_list)
    + np.array(saltbridge_list),
    label="$\pi$-$\pi$",
    color="purple",
)
p6 = plt.bar(
    ind,
    cationpi_list,
    width,
    bottom=np.array(hydrophobic_list)
    + np.array(pipi_list)
    + np.array(hbond_list)
    + np.array(saltbridge_list),
    label="Cation-$\pi$",
    color="orange",
)


# Add some text for labels, title and custom x-axis tick labels, etc.
plt.ylabel("Number of Interactions", fontsize=16)
plt.xlabel("Percent Cutoff", fontsize=16)
plt.title("Interactions in MD-Generated Network", fontsize=20)

plt.xticks(ind, labels, fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=14)

plt.tight_layout()
plt.show()
# make a bar graph where x axis is the number of frames and y axis is the number of shared contacts

# Create a figure and axis
fig, ax1 = plt.subplots()
labels = ["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "95"]
# Create bar plot for frame counts
ax1.bar(
    labels,
    net_len_list,
    alpha=0.7,
    color="slateblue",
    edgecolor="darkslateblue",
    label="Contact from MD",
)
ax1.set_xlabel("Percent Cutoff for the Number of MD Frames", fontsize=14)
ax1.set_ylabel("Number of Contacts", color="darkslateblue", fontsize=16)
ax1.tick_params("y", colors="darkslateblue")
ax1.set_ylim(0, max(net_len_list) + 300)  # Adjust the y-axis limits if necessary

ax2 = ax1.twinx()
ax2.plot(
    labels,
    shared_count,
    marker="o",
    linestyle="-",
    color="darkblue",
    label="Similarity Values",
)
ax2.set_ylabel("Similarity Values", color="darkblue", fontsize=16)
ax2.tick_params("y", colors="darkblue")
ax2.set_ylim(0, 1.2)  # Similarity values are between 0 and 1

# Add a horizontal line for the length of the compare_set
crstal_len = len(network_crystal)
ax1.axhline(
    y=crstal_len,
    color="black",
    linestyle="--",
    linewidth=2,
    label="Contacts from Crystal Structure",
)

# Add a legend
ax1.legend(loc="upper left", fontsize=12)
ax2.legend(loc="upper right")
ax1.tick_params(axis="both", labelsize=12)
ax2.tick_params(axis="both", labelsize=12)
# Set the title
plt.title("Contacts Generated with Varying Amount of MD Frames", fontsize=16)

# Show the plot
plt.tight_layout()
plt.show()


# SECOND GRAPH

# Create a figure and axis
fig, ax1 = plt.subplots()
labels = ["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "95"]
# Create bar plot for frame counts
bar_width = 0
crstal_len = len(network_crystal)
line_1 = ax1.axhline(
    y=crstal_len,
    color="mediumvioletred",
    linestyle="--",
    linewidth=2,
    label="Contacts from Crystal Structure",
)
bar1 = ax1.bar(
    np.arange(len(labels)),
    net_len_list,
    alpha=0.7,
    color="limegreen",
    edgecolor="forestgreen",
    label="Contact from MD",
)
print()
bar2 = ax1.bar(
    np.arange(len(labels)) + bar_width,
    shared_count_no_norm,
    alpha=1.0,
    color="white",
    edgecolor="white",
)
bar3 = ax1.bar(
    np.arange(len(labels)) + bar_width,
    shared_count_no_norm,
    alpha=0.7,
    color="midnightblue",
    edgecolor="midnightblue",
    label="Shared Contacts",
)
ax1.set_xticks(np.arange(len(labels)) + bar_width / 2)
ax1.set_xticklabels(labels)

ax1.set_xlabel("Percent Cutoff for the Number of MD Frames", fontsize=14)
ax1.set_ylabel("Number of Contacts", color="black", fontsize=16)
ax1.tick_params("y", colors="black")
# ax1.set_ylim(0, max(net_len_list) )  # Adjust the y-axis limits if necessary

# Add a horizontal line for the length of the compare_set
# ax1.axhline(
#    y=crstal_len,
#    color="mediumvioletred",
#    linestyle="--",
#    linewidth=2,
#    label="Contacts from Crystal Structure",
# )

# Add a legend
ax1.legend(loc="upper right", fontsize=12)
ax1.tick_params(axis="both", labelsize=12)
# Set the title
plt.title("Contacts Generated with Varying Amount of MD Frames", fontsize=16)

# Show the plot
plt.tight_layout()
plt.show()


md_0_df = pd.DataFrame(columns=["res1", "res2", "score"])
md_90_df = pd.DataFrame(columns=["res1", "res2", "score"])
md_50_df = pd.DataFrame(columns=["res1", "res2", "score"])
md_10_df = pd.DataFrame(columns=["res1", "res2", "score"])
md_95_df = pd.DataFrame(columns=["res1", "res2", "score"])

md_0_res1 = []
md_0_res2 = []
md_0_score = []
md_10_res1 = []
md_10_res2 = []
md_10_score = []
md_90_res1 = []
md_90_res2 = []
md_90_score = []
md_95_res1 = []
md_95_res2 = []
md_95_score = []
md_50_res1 = []
md_50_res2 = []
md_50_score = []
for i in range(TOTAL_RES_NUMBER):
    for j in range(TOTAL_RES_NUMBER):
        if (i, j) in network_md_0:
            md_0_res1.append(i)
            md_0_res2.append(j)
            md_0_score.append(network_md_0[i, j])
        if (i, j) in network_md_95:
            md_95_res1.append(i)
            md_95_res2.append(j)
            md_95_score.append(network_md_95[i, j])
        if (i, j) in network_md_90:
            md_90_res1.append(i)
            md_90_res2.append(j)
            md_90_score.append(network_md_90[i, j])
        if (i, j) in network_md_10:
            md_10_res1.append(i)
            md_10_res2.append(j)
            md_10_score.append(network_md_10[i, j])
        if (i, j) in network_md_50:
            md_50_res1.append(i)
            md_50_res2.append(j)
            md_50_score.append(network_md_50[i, j])

md_10_df["res1"] = md_10_res1
md_10_df["res2"] = md_10_res2
md_10_df["score"] = md_10_score
md_0_df["res1"] = md_0_res1
md_0_df["res2"] = md_0_res2
md_0_df["score"] = md_0_score
md_90_df["res1"] = md_90_res1
md_90_df["res2"] = md_90_res2
md_90_df["score"] = md_90_score
md_95_df["res1"] = md_95_res1
md_95_df["res2"] = md_95_res2
md_95_df["score"] = md_95_score
md_50_df["res1"] = md_50_res1
md_50_df["res2"] = md_50_res2
md_50_df["score"] = md_50_score

md_crystal_net_10 = {}
md_crystal_colors_10 = {}
md_crystal_net_50 = {}
md_crystal_colors_50 = {}
crystal_05 = {}
crystal_05_colors = {}
md_50_05 = {}
md_50_05_colors = {}
for contact, value in network_crystal.items():
    if value >= 0.0:
        crystal_05[contact] = value
        crystal_05_colors[contact] = colors_crystal[contact]

        md_crystal_net_50[contact] = value
        md_crystal_net_10[contact] = value
        if contact not in network_md_10:
            md_crystal_colors_10[contact] = "hotpink"
        else:
            md_crystal_colors_10[contact] = "deepblue"
        if contact not in network_md_50:
            md_crystal_colors_50[contact] = "hotpink"
        else:
            md_crystal_colors_50[contact] = "deepblue"
for contact, value in network_md_10.items():
    if value >= 0.0:
        if contact not in network_crystal:
            md_crystal_net_10[contact] = value
            md_crystal_colors_10[contact] = "green"
for contact, value in network_md_50.items():
    if value >= 0.0:
        md_50_05[contact] = value
        md_50_05_colors[contact] = colors_md_50[contact]

        if contact not in network_crystal:
            md_crystal_net_50[contact] = value
            md_crystal_colors_50[contact] = "green"

FILENAME_PYMOL = "md_crystal_50_all_deepblue.pml"
# project_pymol_res_res_scores(md_crystal_net_50, FILENAME_PYMOL, md_crystal_colors_50)
FILENAME_PYMOL = "md_crystal_10_all_deepblue.pml"
# project_pymol_res_res_scores(md_crystal_net_10, FILENAME_PYMOL, md_crystal_colors_10)
FILENAME_PYMOL = "md_all_50.pml"
# project_pymol_res_res_scores(md_50_05, FILENAME_PYMOL, md_50_05_colors)
FILENAME_PYMOL = "crystal_05.pml"
# project_pymol_res_res_scores(crystal_05, FILENAME_PYMOL, crystal_05_colors)

grid_crystal = toolsnet.make_grid(network_crystal, TOTAL_RES_NUMBER)
grid_md_10 = toolsnet.make_grid(network_md_10, TOTAL_RES_NUMBER)
grid_md_50 = toolsnet.make_grid(network_md_50, TOTAL_RES_NUMBER)
grid_md_90 = toolsnet.make_grid(network_md_90, TOTAL_RES_NUMBER)

toolsnet.plot_int_map(grid_crystal, "Contacts from Crystal Structures")
toolsnet.plot_int_map(grid_md_10, "Contacts from MD Simulations")
toolsnet.plot_int_map(
    grid_md_50, "Contacts from MD Simulation (contact is in 50% of frames)"
)
toolsnet.plot_int_map(
    grid_md_90, "Contacts from md simulation (contact is in 90% of frames)"
)
quit()
FILENAME_HIST = "hist_crystal.pdf"
toolsnet.plot_hist_of_contacts(
    network_crystal,
    "Contact conservation score from crystal structure",
    filename,
    color_choice="red",
)
FILENAME_HIST = "hist_md_10.pdf"
toolsnet.plot_hist_of_contacts(
    network_md_10,
    "Contact conservation score from md (contact is in 10% of frames)",
    filename,
    color_choice="green",
)
FILENAME_HIST = "hist_md_50.pdf"
toolsnet.plot_hist_of_contacts(
    network_md_50,
    "Contact conservation score from md (contact is in 50% of frames)",
    filename,
    color_choice="blue",
)
FILENAME_HIST = "hist_md_90.pdf"
toolsnet.plot_hist_of_contacts(
    network_md_90,
    "Contact conservation score from md (contact is in 90% of frames)",
    filename,
    color_choice="orchid",
)
FILENAME_PYMOL = "tem1_crystal.pml"
project_pymol_res_res_scores(network_crystal, FILENAME_PYMOL, colors_crystal)
FILENAME_PYMOL = "tem1_md_10.pml"
project_pymol_res_res_scores(network_md_10, FILENAME_PYMOL, colors_md_10)
FILENAME_PYMOL = "tem1_md_50.pml"
project_pymol_res_res_scores(network_md_50, FILENAME_PYMOL, colors_md_50)
FILENAME_PYMOL = "tem1_md_90.pml"
project_pymol_res_res_scores(network_md_90, FILENAME_PYMOL, colors_md_50)

corr_coef_90, _ = pearsonr(grid_crystal.flatten(), grid_md_90.flatten())
corr_coef_50, _ = pearsonr(grid_crystal.flatten(), grid_md_50.flatten())
corr_coef_10, _ = pearsonr(grid_crystal.flatten(), grid_md_10.flatten())
print("Correlation coefficient for 90% of frames: ", corr_coef_90)
print("Correlation coefficient for 50% of frames: ", corr_coef_50)
print("Correlation coefficient for 10% of frames: ", corr_coef_10)
