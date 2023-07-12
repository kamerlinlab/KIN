"""This file takes in contacts updated with the msa indexing, compares
the presence of contacts between the structures and outputs a count that
tells the frequency of each contact appearing in the set.
For the interaction type filtering, current clasification is based on the 
interactions of TEM1 such that the network caqn be projected onto its structure"""

from itertools import chain
from collections import Counter
import glob
import os
import pandas as pd


filtered_dfs = []
msa_df_files = glob.glob(
    "/Users/dariiayehorova/lk_research/tools/tools-project/contact_analysis/multi_structure_test/msa_outputs/*.csv"
)
network_files = glob.glob(
    "/Users/dariiayehorova/lk_research/tools/tools-project/contact_analysis/multi_structure_test/network_output/*.csv"
)
msa_columns = ["Res1_msa", "Res2_msa"]
STRUCTURE_COUNT = 0
INTERACTION_COUNT = 0
THRESHOLD = 1.0


for file_path in msa_df_files:
    STRUCTURE_COUNT += 1
    df = pd.read_csv(file_path)
    df_filter = df[msa_columns]
    filtered_dfs.append(df_filter)
# Combining filtered dataframes into a list of tuples,
# where each tuple is a contact based on msa indx
combined_data = list(
    chain.from_iterable(
        df_filtered.itertuples(index=False) for df_filtered in filtered_dfs
    )
)
pair_counts = Counter(combined_data)
selected_contacts = pd.DataFrame({"Res1_msa": [], "Res2_msa": []})
res1_selected = []
res2_selected = []

for pair, count in pair_counts.items():
    if count / STRUCTURE_COUNT >= THRESHOLD:
        INTERACTION_COUNT += 1
        res1_selected.append(pair[0])
        res2_selected.append(pair[1])
selected_contacts["Res1_msa"] = res1_selected
selected_contacts["Res2_msa"] = res2_selected

print(
    f"There are {INTERACTION_COUNT} interactions that occur in the {THRESHOLD*100}% of structures"
)
print(f"Total number of structures:{STRUCTURE_COUNT}")
print(f"This interaction occure in {STRUCTURE_COUNT*THRESHOLD} structures")

# Compare to the interactions of the TEM-1 and reduce the network only to
# the types of interactions present in TEM-1

for file_path in msa_df_files:
    df = pd.read_csv(file_path)
    merged_dataframe = pd.merge(selected_contacts, df, on=msa_columns)

    file_name = os.path.basename(file_path)
    file_name_without_extension = os.path.splitext(file_name)[0]

    NETWORK_OUTPUT = "network_output/" + file_name_without_extension + "_no_type.csv"
    merged_dataframe.to_csv(NETWORK_OUTPUT, index=False)

    if file_path.endswith("1M40_TEM-1_msa.csv"):
        TEM1_df = merged_dataframe


for file_path in network_files:
    df = pd.read_csv(file_path)

    merged_dataframe = pd.merge(
        df, TEM1_df, on=["Interaction_Type", "Res1_msa", "Res2_msa"]
    )
    file_name = os.path.basename(file_path)
    file_name_without_extension = os.path.splitext(file_name)[0]
    print(
        file_name,
        ": preserved interactions with the same interaction type as TEM",
        merged_dataframe.shape[0],
    )
    NETWORK_OUTPUT = (
        "network_output/proj_1M40_TEM-1/" + file_name_without_extension + ".csv"
    )
    merged_dataframe.to_csv(NETWORK_OUTPUT, index=False)
