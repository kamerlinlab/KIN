"""This file takes in contacts updated with the msa indexing, compares
the presence of contacts between the structures and outputs a count that
tells the frequency of each contact appearing in the set.
For the interaction type filtering, current clasification is based on the 
interactions of TEM1 such that the network caqn be projected onto its structure"""

from itertools import chain
from collections import Counter
import glob
import os
from re import I
import pandas as pd


filtered_dfs = []
msa_df_files = glob.glob(
    "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/multi_structure_test/msa_outputs/*.csv"
)
network_files = glob.glob(
    "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/multi_structure_test/network_output/*.csv"
)
msa_columns = ["Res1_msa", "Res2_msa"]
structure_count = 0
interaction_count = 0
THRESHOLD = 1.0
TARGET_STRUCTURE = "1M40_TEM-1_msa"
all_interactions_dict = {}
all_interactions_dfs = {}
for file_path in msa_df_files:
    structure_count += 1
    df = pd.read_csv(file_path)
    df_filter = df[msa_columns]
    filtered_dfs.append(df_filter)

    file_name = os.path.basename(file_path)
    system_name = os.path.splitext(file_name)[0]

    all_interactions_dict[system_name] = {}
    all_interactions_dfs[system_name] = df
    res1_msa_list = list(df["Res1_msa"])
    res2_msa_list = list(df["Res2_msa"])
    int_type_list = list(df["Interaction_Type"])
    int_location = list(df["Residue_Parts"])
    all_interactions_list = []

    if system_name == TARGET_STRUCTURE:
        target_msa_pdb = {}
        res1_pdb_list = list(df["Res1"])
        res2_pdb_list = list(df["Res2"])
        for index, res1 in enumerate(res1_pdb_list):
            target_msa_pdb[(res1_msa_list[index], res2_msa_list[index])] = (
                res1_pdb_list,
                res2_pdb_list,
            )

    for index, res_1_msa in enumerate(df["Res1_msa"]):
        all_interactions_list.append(
            (res_1_msa, res2_msa_list[index])
        )
    all_interactions_dict[system_name] = all_interactions_list


def conservation_nextwork_dict(
    all_int_dict: dict,
    target_msa_pdb_dict: dict,
    target_structure: str,
    index_type: str,
) -> dict:
    """Takes in all the contacts in the form of a dictionary, compares it to the structure of the
    target to make sure that the contacts that are not present are not due to the missing residues,
    and outputs a dictionary of conservation scores in the desired indexing.
    """
    target_contacts = all_int_dict[target_structure]
    for strucutre, contacts in all_int_dict.items():
        for contact in contacts:
            res1_msa = contact[0]
            res2_msa = contact[1]
        if 
    if index_type == "msa":
        dir_out = conservations_msa
    elif index_type == "pdb":
        dir_out = conservations_pdb
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
    return dir_out


def conservation_nextwork_df(
    all_int_df: dict(pd.DataFrame),
    target_msa_pdb_dict: dict,
    target_structure: str,
    index_type: str,
) -> dict:
    """Takes in all the contacts in the form of a dictionary, compares it to the structure of the
    target to make sure that the contacts that are not present are not due to the missing residues,
    and outputs a dictionary of conservation scores in the desired indexing.
    """
    target_contacts = all_int_df[target_structure]
    for strucutre, contacts in all_int_dict.items():
        for contact in contacts:
            res1_msa = contact[0]
            res2_msa = contact[1]

            print(res1_msa)
        quit()
    if index_type == "msa":
        dir_out = conservations_msa
    elif index_type == "pdb":
        dir_out = conservations_pdb
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
    return dir_out



conservation_tem_msa = conservation_nextwork_dict(
    all_interactions_dict, target_msa_pdb, TARGET_STRUCTURE, index_type="msa"
)
quit()
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
    if count / structure_count >= THRESHOLD:
        interaction_count += 1
        res1_selected.append(pair[0])
        res2_selected.append(pair[1])
selected_contacts["Res1_msa"] = res1_selected
selected_contacts["Res2_msa"] = res2_selected

print(
    f"There are {interaction_count} interactions that occur in the {THRESHOLD*100}% of structures"
)
print(f"Total number of structures:{structure_count}")
print(f"This interaction occure in {structure_count*THRESHOLD} structures")

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
        TEM1_df = merged_dataframe[["Interaction_Type", "Res1_msa", "Res2_msa"]]


for file_path in network_files:
    df = pd.read_csv(file_path)

    merged_dataframe = pd.merge(
        TEM1_df, df, on=["Interaction_Type", "Res1_msa", "Res2_msa"]
    )
    file_name = os.path.basename(file_path)
    file_name_without_extension = os.path.splitext(file_name)[0]
    print(
        file_name,
        ": preserved interactions of TEM type",
        merged_dataframe.shape[0],
    )
    NETWORK_OUTPUT = (
        "network_output/proj_1M40_TEM-1/" + file_name_without_extension + ".csv"
    )
    merged_dataframe.to_csv(NETWORK_OUTPUT, index=False)
