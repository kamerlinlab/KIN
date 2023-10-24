"""This file takes in contacts updated with the msa indexing,
and outputs a network of contacts shared among all the structures
along with their conservation scores. """

import csv
from re import I

from matplotlib import colors
from tools_proj.pymol_projections import project_pymol_res_res_scores
from tools_proj.pymol_projections import project_pymol_per_res_scores
from tools_proj.msa_network import common_network
from tools_proj.msa_network import plot_per_res_score
from matplotlib import pyplot as plt


input_fiels_0 = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/msa_index_contacts/retention_0"
input_fiels_10 = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/msa_index_contacts/retention_10"
input_fiels_20 = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/msa_index_contacts/retention_20"
input_fiels_30 = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/msa_index_contacts/retention_30"
input_fiels_40 = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/msa_index_contacts/retention_40"
input_fiels_50 = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/msa_index_contacts/retention_50"
input_fiels_60 = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/msa_index_contacts/retention_60"
input_fiels_70 = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/msa_index_contacts/retention_70"
input_fiels_80 = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/msa_index_contacts/retention_80"
input_fiels_90 = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/msa_index_contacts/retention_90"
input_fiels_95 = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/msa_index_contacts/retention_95"
contact_index = "pdb"
input_files_list = [
    input_fiels_0,
    input_fiels_10,
    input_fiels_20,
    input_fiels_30,
    input_fiels_40,
    input_fiels_50,
    input_fiels_60,
    input_fiels_70,
    input_fiels_80,
    input_fiels_90,
    input_fiels_95,
]
for input_files in input_files_list:
    (
        conservation_tem_msa,
        colors_int_type,
        properties,
        miss_net,
        miss_colors,
        miss_prop,
    ) = common_network(
        input_files,
        "1M40_TEM-1",
        contact_index,
        missing_network=True,
        no_vdw=True,
        only_sc=True,
    )
    retention = input_files.split("/")[-1]
    retention_number = retention.split("_")[-1]
    projection_output = (
        f"shared_network/1M40_TEM-1_network_sc_nvw_{retention_number}.pml"
    )
    miss_projection = f"missing_network/tem1_missing_sc_nvw_{retention_number}.pml"
    miss_projection_50 = (
        f"missing_network/tem1_missing_nvw_sc_50_{retention_number}.pml"
    )
    properties_filename = (
        f"shared_network/properties_tem1_sc_nvw_{retention_number}.csv"
    )
    if contact_index == "pdb":
        project_pymol_res_res_scores(
            conservation_tem_msa, projection_output, colors_int_type
        )
        project_pymol_res_res_scores(miss_net, miss_projection, miss_colors)
        miss_net_50 = {}
        miss_colors_50 = {}
        sc_no_hydrophobic = {}
        sc_no_hydrophobic_colors = {}
        per_res_score = {}
        per_res_score_colors = {}
        high_scores = []
        for key, value in conservation_tem_msa.items():
            if colors_int_type[key] != "br9":
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
            per_res_score[key] = (per_res_score[key] - min_score) / (
                max_score - min_score
            )

            if value > 0.9:
                high_scores.append(key)
        print(sorted(high_scores))
        # project_pymol_per_res_scores(
        #    per_res_score, f"shared_network/per_res_sc_nohydro{retention_number}.pml"
        # )
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
            f"KIN scores per residue for TEM-1 analysis with {retention_number} MD retention",
        )
        # project_pymol_res_res_scores(
        #    sc_no_hydrophobic,
        #    f"shared_network/sc_no_hydrophobic_sc_nvw_{retention_number}.pml",
        #    sc_no_hydrophobic_colors,
        # )
        for key, value in miss_net.items():
            if value >= 0.5:
                miss_net_50[key] = value
                miss_colors_50[key] = miss_colors[key]
        # project_pymol_res_res_scores(miss_net_50, miss_projection_50, miss_colors_50)

        output_filename = (
            f"shared_network/network_tem1_pdb_nvw_sc_{retention_number}.csv"
        )
        colors_file = f"shared_network/colors_tem1_pdb_sc_nvw_{retention_number}.csv"
    else:
        output_filename = (
            f"shared_network/network_tem1_msa_sc_nvw_{retention_number}.csv"
        )
    print(retention_number)
    if retention_number == "20":
        quit()
quit()
#    counter_10 = 0
#    counter_90 = 0
#    counter_99 = 0
#    for key, value in conservation_tem_msa.items():
#        if value >= 0.5:
#            counter_10 += 1
#        if value >= 0.9:
#            counter_90 += 1
#        if value >= 0.99:
#            counter_99 += 1
#    print(input_files)
#    print("Number of contacts with conservation score >= 0.5: ", counter_10)
#    print("Number of contacts with conservation score >= 0.9: ", counter_90)
#    print("Number of contacts with conservation score >= 0.99: ", counter_99)
#
#    with open(output_filename, "w", newline="") as csvfile:
#        csv_writer = csv.DictWriter(csvfile, fieldnames=conservation_tem_msa.keys())
#        csv_writer.writeheader()
#        csv_writer.writerow(conservation_tem_msa)
#
#    properties.to_csv(properties_filename, index=False)
#
#    if contact_index == "pdb":
#        with open(colors_file, "w", newline="") as csvfile:
#            csv_writer = csv.DictWriter(csvfile, fieldnames=colors_int_type.keys())
#            csv_writer.writeheader()
#            csv_writer.writerow(colors_int_type)
