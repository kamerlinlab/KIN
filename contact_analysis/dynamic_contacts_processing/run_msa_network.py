"""This file takes in contacts updated with the msa indexing,
and outputs a network of contacts shared among all the structures
along with their conservation scores. """

import csv
from tools_proj.pymol_projections import project_pymol_res_res_scores
from tools_proj.msa_network import common_network


input_fiels_0 = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/msa_index_contacts/retention_0"
input_fiels_10 = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/msa_index_contacts/retention_10"
input_fiels_50 = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/msa_index_contacts/retention_50"
input_fiels_90 = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/msa_index_contacts/retention_90"
contact_index = "pdb"
input_files_list = [input_fiels_0, input_fiels_10, input_fiels_50, input_fiels_90]
for input_files in input_files_list:
    conservation_tem_msa, colors_int_type, properties, _, _, _ = common_network(
        input_files, "1M40_TEM-1", contact_index, no_vdw=True, only_sc=False
    )
    retention = input_files.split("/")[-1]
    retention_number = retention.split("_")[-1]
    projection_output = f"1M40_TEM-1_network_{retention_number}.pml"
    properties_filename = f"properties_tem1_nv_{retention_number}.csv"
    if contact_index == "pdb":
        # project_pymol_res_res_scores(
        #        conservation_tem_msa, projection_output, colors_int_type
        #    )
        output_filename = f"network_tem1_pdb_nv_{retention_number}.csv"
        colors_file = f"colors_tem1_pdb_nv_{retention_number}.csv"
    else:
        output_filename = f"network_tem1_msa_nv_{retention_number}.csv"

    counter_10 = 0
    counter_90 = 0
    counter_99 = 0
    for key, value in conservation_tem_msa.items():
        if value >= 0.5:
            counter_10 += 1
        if value >= 0.9:
            counter_90 += 1
        if value >= 0.99:
            counter_99 += 1

    print("Number of contacts with conservation score >= 0.5: ", counter_10)
    print("Number of contacts with conservation score >= 0.9: ", counter_90)
    print("Number of contacts with conservation score >= 0.99: ", counter_99)

    with open(output_filename, "w", newline="") as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=conservation_tem_msa.keys())
        csv_writer.writeheader()
        csv_writer.writerow(conservation_tem_msa)

    properties.to_csv(properties_filename, index=False)

    if contact_index == "pdb":
        with open(colors_file, "w", newline="") as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=colors_int_type.keys())
            csv_writer.writeheader()
            csv_writer.writerow(colors_int_type)
