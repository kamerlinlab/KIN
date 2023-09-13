from fileinput import filename
from scipy.stats import pearsonr
from tools_proj.pymol_projections import project_pymol_res_res_scores
import tools_proj.msa_network as toolsnet


network_crystal_file = "static_contacts_processing/shared_network/network_tem1_pdb.csv"
colors_crystal_file = "static_contacts_processing/shared_network/colors_tem1_pdb.csv"
network_crystal_file = "static_contacts_processing/shared_network/network_tem1_pdb.csv"
colors_crystal_file = "static_contacts_processing/shared_network/colors_tem1_pdb.csv"
network_md_file_90 = (
    "dynamic_contacts_processing/shared_network/network_tem1_pdb_90.csv"
)
colors_md_file_90 = "dynamic_contacts_processing/shared_network/colors_tem1_pdb_90.csv"
network_md_file_50 = (
    "dynamic_contacts_processing/shared_network/network_tem1_pdb_50.csv"
)
colors_md_file_50 = "dynamic_contacts_processing/shared_network/colors_tem1_pdb_50.csv"
network_md_file_10 = (
    "dynamic_contacts_processing/shared_network/network_tem1_pdb_10.csv"
)
colors_md_file_10 = "dynamic_contacts_processing/shared_network/colors_tem1_pdb_10.csv"

TOTAL_RES_NUMBER = 263

network_crystal = toolsnet.get_contacts_from_csv(network_crystal_file)
network_md_10 = toolsnet.get_contacts_from_csv(network_md_file_10)
network_md_50 = toolsnet.get_contacts_from_csv(network_md_file_50)
network_md_90 = toolsnet.get_contacts_from_csv(network_md_file_90)
colors_crystal = toolsnet.get_contacts_from_csv(colors_crystal_file, value_type=str)
colors_md_10 = toolsnet.get_contacts_from_csv(colors_md_file_10, value_type=str)
colors_md_50 = toolsnet.get_contacts_from_csv(colors_md_file_50, value_type=str)
colors_md_90 = toolsnet.get_contacts_from_csv(colors_md_file_90, value_type=str)

grid_crystal = toolsnet.make_grid(network_crystal, TOTAL_RES_NUMBER)
grid_md_10 = toolsnet.make_grid(network_md_10, TOTAL_RES_NUMBER)
grid_md_50 = toolsnet.make_grid(network_md_50, TOTAL_RES_NUMBER)
grid_md_90 = toolsnet.make_grid(network_md_90, TOTAL_RES_NUMBER)

toolsnet.plot_int_map(grid_crystal, "Contacts from crystal structure")
toolsnet.plot_int_map(
    grid_md_10, "Contacts from md simulation (contact is in 10% of frames)"
)
toolsnet.plot_int_map(
    grid_md_50, "Contacts from md simulation (contact is in 50% of frames)"
)
toolsnet.plot_int_map(
    grid_md_90, "Contacts from md simulation (contact is in 90% of frames)"
)
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
