"""Script to handle projection of the new contact format onto the """

import pandas as pd

TEM_FILE = "network_output/1M40_TEM-1_msa_no_type.csv"
tem_df = pd.read_csv(TEM_FILE)

INT_COLORS = {
    "vdw": "br9",
    "hydrophobic": "green",
    "saltbridge": "br1",
    "cationpi": "ruby",
    "pipi": "orange",
    "hbonds": "gray",
}
INT_RADIUS = {
    "mc-mc": 0.3,
    "mc-wc": 0.3,
    "wc-wc": 0.3,
    "wc-sc": 0.3,
    "sc-sc": 0.3,
    "sc_mc": 0.3,
    "mc_sc": 0.3,
}
out_file_contents = ""
out_file_contents += (
    "# You can run me in several ways, perhaps the easiest way is to:\n"
)
out_file_contents += "# 1. Load the PDB file of your system in PyMOL.\n"
out_file_contents += "# 2. Type: @[FILE_NAME.py] in the command line.\n"
out_file_contents += (
    "# 3. Make sure the .py files are in the same directory as the pdb.\n"
)

for index in tem_df.index:
    RES1 = str(tem_df.loc[index, "Res1"])
    RES1_INDX = RES1[3:]
    RES2 = str(tem_df.loc[index, "Res2"])
    RES2_INDX = RES2[3:]
    INT_TYPE = str(tem_df.loc[index, "Interaction_Type"])
    RES_PART = str(tem_df.loc[index, "Residue_Parts"])
    color = INT_COLORS[INT_TYPE]
    radius = INT_RADIUS[RES_PART]
    feature_rep = (
        f"distance interaction{index+1}, "
        + f"resid {RES1_INDX} and name CA, "
        + f"resid {RES2_INDX} and name CA \n"
        f"set dash_radius, {radius}, interaction{index+1} \n"
        f"set dash_color, {color}, interaction{index+1} \n"
    )
    out_file_contents += feature_rep

# Finally, group all draw interactions made together,
# (easier for a user to handle in PyMOL)
out_file_contents += "group All_Interactions, interaction* \n"
out_file_contents += "set dash_gap, 0.00, All_Interactions \n"
out_file_contents += "set dash_round_ends, on, All_Interactions \n"
out_file_contents += "hide labels \n"

OUT_FILE_SAFE = "TEM_network.pml"
with open(OUT_FILE_SAFE, "w+", encoding="utf-8") as file_out:
    file_out.write(out_file_contents)
print(f"The file: {OUT_FILE_SAFE} was written to disk.")
