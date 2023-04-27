"""
Script to extract and download all unique class A beta lactamase structures
from the database available at: http://www.bldb.eu/S-BLDB.php

The script removes non-natural structures and for enzymes with multiple
duplicates, the structure with the lowest resolution value is kept.
Note: Highest/best resolution structure is one with lowest resolution value.

Each pdb file is then downloaded from the protein databank and stored
inside a folder named: "pdb_files"
"""
import os
from time import sleep
import urllib.request
import pandas as pd
import numpy as np


TABLE_URL = r"http://www.bldb.eu/S-BLDB.php"
OUTPUT_FOLDER = "pdb_files"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# download table.
all_blactam_df = pd.read_html(TABLE_URL)[1]

class_A_blactam = all_blactam_df[all_blactam_df["Amblerclass"] == "A"]
print(f" Number of Class A structures found: {len(class_A_blactam)}")

# remove non-needed columns
drop_list = ["Amblerclass", "Releasedate", "PubMedID", "DOI", "PDB", "Mutations",
             "Ligands", "Spacegroup", "Unit cell parameters", "Zvalue"]
class_A_blactam = class_A_blactam.drop(drop_list, axis=1)

# Proteins without uniprot information are synthetic or from ancestral reconstruction.
# These will therefore not be included.
class_A_blactam = class_A_blactam.dropna()

# There are also a few chimeric structures, which should not be included.
remove_mask = class_A_blactam["PDBcode"].isin(
    ["4ID4", "4QY5", "4QY6", "4R4R", "4R4S", ]
)
class_A_blactam = class_A_blactam[~remove_mask]

print(f"Number of Natural class A structures found: {len(class_A_blactam)}")
num_unique = len(class_A_blactam["Proteinname"].unique())
print(f" Number of UNIQUE, Natural class A structures found: {num_unique}")


# Now filter the df to keep only the structure with lowest resolution score.
# Preorder each unique enzyme to have lowest resolution structure
# first for easy filtering with drop duplicates.
class_A_blactam = class_A_blactam.sort_values(
    ["Proteinname", "Resolution(Å)"],
    ascending=[True, True]
)

structs_to_sim = class_A_blactam.drop_duplicates(
    subset=["Proteinname"],
    keep="first"
)

# save info about the selected structures.
file_path = OUTPUT_FOLDER + r"/" + "structures_to_simulate.csv"
structs_to_sim.to_csv(file_path, index=False)


# Part 2: Download from the PDB
pdbs_to_get = dict(
    zip(structs_to_sim["PDBcode"], structs_to_sim["Proteinname"]))
print(f"Number of pdbs to download:{len(pdbs_to_get)}")


for pdb_id, enzyme_name in pdbs_to_get.items():

    # download file.
    url = "https://files.rcsb.org/download/" + pdb_id + ".pdb"

    with urllib.request.urlopen(url) as response:
        data = response.read()
    text = data.decode("utf-8")

    # save text
    pdb_file = OUTPUT_FOLDER + r"/" + pdb_id + "_" + enzyme_name + ".pdb"
    with open(pdb_file, "w", encoding="utf-8") as text_file:
        text_file.write(text)

    print(f"saved file: {pdb_file}")

    # Adding as a just in case to not send too many requests at once.
    sleeptime = np.random.uniform(0.5, 1.5)
    sleep(sleeptime)
