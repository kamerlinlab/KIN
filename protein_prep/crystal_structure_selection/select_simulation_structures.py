"""
Script to extract all unique class A beta lactmase structures
from the database available at: http://www.bldb.eu/S-BLDB.php

The script removes non-natural structures and for enzymes with multiple
duplicates, the structure with the lowest resolution value is kept.
"""
import pandas as pd

# download table.
table_url = r"http://www.bldb.eu/S-BLDB.php"
all_blactam_df = pd.read_html(table_url)[1]

class_A_blactam = all_blactam_df[all_blactam_df["Amblerclass"] == "A"]
print(f" Number of Class A structures found: {len(class_A_blactam)}")

# remove non-needed columns
drop_list = ["Amblerclass", "Releasedate", "PubMedID", "DOI", "PDB", "Mutations",
             "Ligands", "Spacegroup", "Unit cell parameters", "Zvalue"]
class_A_blactam = class_A_blactam.drop(drop_list, axis=1)

# Proteins without uniprot information are synthetic or from ancestral reconstruction.
# These will therefore not be included.
class_A_blactam = class_A_blactam.dropna()
print(f"Number of Natural class A structures found: {len(class_A_blactam)}")
num_unique = len(class_A_blactam["Proteinname"].unique())
print(f" Number of UNIQUE, Natural class A structures found: {num_unique}")


# Now filter the df to keep only the structure with lowest resolution.
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

# save as complete.
structs_to_sim.to_csv("structures_to_simulate.csv", index=False)
