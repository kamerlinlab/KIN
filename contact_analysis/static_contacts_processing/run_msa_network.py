"""This file takes in contacts updated with the msa indexing,
and outputs a network of contacts shared among all the structures
along with their conservation scores. """

import csv
from kin.pymol_projections import project_pymol_res_res_scores
from kin.msa_network import common_network
from kin.msa_network import plot_hist_of_contacts as his
from kin.pymol_projections import project_pymol_per_res_scores
from kin.msa_network import plot_per_res_score

input_fiels = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/static_contacts_processing/msa_index_contacts/"
projection_output = "shared_network/1M40_TEM-1_sc_nvw_network.pml"
miss_projected = "missing_network/tem1-missing_sc_nvw_network.pml"
contact_index = "pdb"

(
    conservation_tem_msa,
    colors_int_type,
    props,
    miss_net,
    miss_colors,
    miss_prop,
) = common_network(
    input_fiels,
    "1M40_TEM-1",
    contact_index,
    missing_network=True,
    no_vdw=True,
    only_sc=True,
)
if contact_index == "pdb":
    project_pymol_res_res_scores(
        conservation_tem_msa, projection_output, colors_int_type
    )
    project_pymol_res_res_scores(miss_net, miss_projected, miss_colors)
    output_filename = "shared_network/network_tem1_sc_nvw_pdb.csv"
    colors_file = "shared_network/colors_tem1_sc_nvw_pdb.csv"
    miss_output_filename = "miss_tem1_sc_nvw_pdb.csv"
    miss_colors_file = "miss_colors_tem1_sc_nvw_pdb.csv"
    miss_prop_file = "miss_prop_tem1_sc_nvw_pdb.csv"
    prop_file = "shared_network/prop_tem1_sc_nvw_pdb.csv"
    sc_no_hydrophobic = {}
    sc_no_hydrophobic_colors = {}
    per_res_score = {}
    for key, value in conservation_tem_msa.items():
        if colors_int_type[key] != "br9":
            print(key)
            sc_no_hydrophobic[key] = value
            sc_no_hydrophobic_colors[key] = colors_int_type[key]
            if key[0] in per_res_score.keys():
                per_res_score[key[0]] += value
            else:
                per_res_score[key[0]] = value
            if key[1] in per_res_score.keys():
                per_res_score[key[1]] += value
            else:
                per_res_score[key[1]] = value

    max_score = max(per_res_score.values())
    min_score = min(per_res_score.values())
    for key, value in per_res_score.items():
        per_res_score[key] = (per_res_score[key] - min_score) / (max_score - min_score)
    project_pymol_per_res_scores(per_res_score, f"shared_network/per_res_sc.pml")
    active_res = [45, 141]
    close_res = [
        44,
        45,
        46,
        48,
        79,
        80,
        105,
        107,
        141,
        145,
        209,
        210,
        211,
        212,
        213,
        214,
        245,
    ]
    plot_per_res_score(
        per_res_score,
        263,
        active_res,
        close_res,
        f"KIN scores per residue for TEM-1 analysis wuth crystal structure",
    )
    quit()
    project_pymol_res_res_scores(
        sc_no_hydrophobic,
        "shared_network/sc_no_hydrophobic_nvw.pml",
        sc_no_hydrophobic_colors,
    )

else:
    output_filename = "shared_network/network_tem1_msa.csv"
print(len(miss_net))
counter_50 = 0
counter_90 = 0
counter_99 = 0
for key, value in conservation_tem_msa.items():
    if value >= 0.5:
        counter_50 += 1
    if value >= 0.9:
        counter_90 += 1
    if value >= 0.99:
        counter_99 += 1

print("Number of contacts with conservation score >= 0.5: ", counter_50)
print("Number of contacts with conservation score >= 0.9: ", counter_90)
print("Number of contacts with conservation score >= 0.95: ", counter_99)

props.to_csv(prop_file, index=False)
# miss_prop.to_csv(miss_prop_file, index=False)
# with open(miss_output_filename, "w", newline="") as csvfile:
#    csv_writer = csv.DictWriter(csvfile, fieldnames=miss_net.keys())
#    csv_writer.writeheader()
#    csv_writer.writerow(miss_net)

# if contact_index == "pdb":
#    with open(miss_colors_file, "w", newline="") as csvfile:
#        csv_writer = csv.DictWriter(csvfile, fieldnames=miss_colors.keys())
#        csv_writer.writeheader()
#        csv_writer.writerow(miss_colors)

with open(output_filename, "w", newline="") as csvfile:
    csv_writer = csv.DictWriter(csvfile, fieldnames=conservation_tem_msa.keys())
    csv_writer.writeheader()
    csv_writer.writerow(conservation_tem_msa)

if contact_index == "pdb":
    with open(colors_file, "w", newline="") as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=colors_int_type.keys())
        csv_writer.writeheader()
        csv_writer.writerow(colors_int_type)
name_miss_hist = "crystal_missing.pdf"
name_hist = "crystal_sc_nvd.pdf"
his(
    miss_net,
    "Distribution of Conservation Scores in the Network of Missing Contacts",
    name_miss_hist,
    color_choice="blue",
)
his(
    conservation_tem_msa,
    "Distribution of Conservation Scores in the Network of Contacts",
    name_hist,
    color_choice="blue",
)
