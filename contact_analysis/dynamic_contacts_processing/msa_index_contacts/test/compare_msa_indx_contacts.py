import numpy as np
import pandas as pd
import tools_proj.msa_network as toolsnet


def shared_network_as_df(network_file: str) -> pd.DataFrame:
    """Takes in a network file and returns a dataframe with columns
    res1, res2, score"""
    network_dict = toolsnet.get_contacts_from_csv(network_file)

    res1_list = []
    res2_list = []
    score_list = []

    for key, value in network_dict.items():
        res1_list.append(key[0])
        res2_list.append(key[1])
        score_list.append(value)

    return pd.DataFrame({"res1": res1_list, "res2": res2_list, "score": score_list})


md_0 = "1BSG_SAL-1_msa_md_0.csv"
md_10 = "1BSG_SAL-1_msa_md_10.csv"
md_50 = "1BSG_SAL-1_msa_md.csv"
md_90 = "1BSG_SAL-1_msa_md_90.csv"

net_pdb_0 = "network_tem1_pdb_nv_new_0.csv"
net_pdb_10 = "network_tem1_pdb_nv_new_10.csv"
net_pdb_50 = "network_tem1_pdb_nv_new_50.csv"
net_pdb_90 = "network_tem1_pdb_nv_new_90.csv"

prop_0_df = pd.read_csv("properties_tem1_msa_new_0.csv")
print("---------------------")
print("retention = 0")
print("---------------------")
print(prop_0_df[prop_0_df["Res1_pdb"] == 47])
print(prop_0_df[prop_0_df["Res2_pdb"] == 47])
prop_10_df = pd.read_csv("properties_tem1_msa_new_10.csv")
print("---------------------")
print("retention = 10")
print("---------------------")
print(prop_10_df[prop_10_df["Res1_pdb"] == 47])
print(prop_10_df[prop_10_df["Res2_pdb"] == 47])
prop_50_df = pd.read_csv("properties_tem1_msa_new_50.csv")
print("---------------------")
print("retention = 50")
print("---------------------")
print(prop_50_df[prop_50_df["Res1_pdb"] == 47])
print(prop_50_df[prop_50_df["Res2_pdb"] == 47])
prop_90_df = pd.read_csv("properties_tem1_msa_new_90.csv")
print("---------------------")
print("retention = 90")
print("---------------------")
print(prop_90_df[prop_90_df["Res1_pdb"] == 47])
print(prop_90_df[prop_90_df["Res2_pdb"] == 47])


net_pdb_0_df = shared_network_as_df(net_pdb_0)
net_pdb_10_df = shared_network_as_df(net_pdb_10)
net_pdb_50_df = shared_network_as_df(net_pdb_50)
net_pdb_90_df = shared_network_as_df(net_pdb_90)

print(net_pdb_0_df[net_pdb_0_df["res1"] == 47])
print(net_pdb_0_df[net_pdb_0_df["res2"] == 47])
print(net_pdb_10_df[net_pdb_10_df["res1"] == 47])
print(net_pdb_10_df[net_pdb_10_df["res2"] == 47])
print(net_pdb_50_df[net_pdb_50_df["res1"] == 47])
print(net_pdb_50_df[net_pdb_50_df["res2"] == 47])
print(net_pdb_90_df[net_pdb_90_df["res1"] == 47])
print(net_pdb_90_df[net_pdb_90_df["res2"] == 47])
quit()

md_0_df = pd.read_csv(md_0)
md_10_df = pd.read_csv(md_10)
md_50_df = pd.read_csv(md_50)
md_90_df = pd.read_csv(md_90)


print(md_0_df[md_0_df["Res1_msa"] == 47])
print(md_0_df[md_0_df["Res2_msa"] == 47])
print(md_10_df[md_10_df["Res1_msa"] == 47])
print(md_10_df[md_10_df["Res2_msa"] == 47])
print(md_50_df[md_50_df["Res1_msa"] == 47])
print(md_50_df[md_50_df["Res2_msa"] == 47])
print(md_90_df[md_90_df["Res1_msa"] == 47])
print(md_90_df[md_90_df["Res2_msa"] == 47])
