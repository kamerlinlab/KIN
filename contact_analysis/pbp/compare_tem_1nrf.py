from fileinput import filename
from re import I
from scipy.stats import pearsonr
from tools_proj.pymol_projections import project_pymol_res_res_scores
import pandas as pd
import tools_proj.msa_network as toolsnet


network_tem_file = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/static_contacts_processing/shared_network/network_tem1_pdb.csv"
colors_tem_file = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/static_contacts_processing/shared_network/colors_tem1_pdb.csv"
network_pbp_file = "network_1nrf_pdb_nv.csv"
colors_pbp_file = "colors_1nrf_pdb_nv.csv"

TOTAL_RES_NUMBER = 263

network_tem = toolsnet.get_contacts_from_csv(network_tem_file)
network_pbp = toolsnet.get_contacts_from_csv(network_pbp_file)
colors_crystal = toolsnet.get_contacts_from_csv(colors_tem_file, value_type=str)
colors_md_10 = toolsnet.get_contacts_from_csv(colors_pbp_file, value_type=str)


md_crystal_net_10 = {}
md_crystal_colors_10 = {}
md_crystal_net_50 = {}
md_crystal_colors_50 = {}
crystal_05 = {}
crystal_05_colors = {}
md_50_05 = {}
md_50_05_colors = {}
tem_pbp = {}
tem_pbp_colors = {}
for contact, value in network_tem.items():
    if contact not in network_pbp:
        tem_pbp[contact] = value
        tem_pbp_colors[contact] = "lightpink"
    else:
        tem_pbp[contact] = value
        tem_pbp_colors[contact] = "lead"
for contact, value in network_pbp.items():
    if contact not in network_tem:
        tem_pbp[contact] = value
        tem_pbp_colors[contact] = "br4"

FILENAME_PYMOL = "tem_pbp.pml"
project_pymol_res_res_scores(tem_pbp, FILENAME_PYMOL, tem_pbp_colors)

grid_pbp = toolsnet.make_grid(network_pbp, TOTAL_RES_NUMBER)

grid_tem = toolsnet.make_grid(network_tem, TOTAL_RES_NUMBER)

toolsnet.plot_int_map(grid_pbp, "Contacts from BlaR penicillin-receptor")
toolsnet.plot_int_map(grid_tem, "Contacts from TEM1 beta-lactamase")
corr_coef, _ = pearsonr(grid_pbp.flatten(), grid_tem.flatten())
print("Correlation coefficient for 90% of frames: ", corr_coef)
quit()
toolsnet.plot_int_map(
    grid_md_50, "Contacts from MD simulation (contact is in 50% of frames)"
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
