"""This file takes in contacts updated with the msa indexing,
and outputs a network of contacts shared among all the structures
along with their conservation scores. """

import csv
from tools_proj.pymol_projections import project_pymol_res_res_scores
from tools_proj.msa_network import common_network


input_fiels = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/msa_index_contacts/retention_90"
projection_output = "1M40_TEM-1_network_90.pml"
contact_index = "pdb"

conservation_tem_msa, colors_int_type = common_network(
    input_fiels, "1M40_TEM-1", contact_index, no_vdw=True, only_sc=False
)
if contact_index == "pdb":
    project_pymol_res_res_scores(
        conservation_tem_msa, projection_output, colors_int_type
    )
    output_filename = "network_tem1_pdb_90.csv"
    colors_file = "colors_tem1_pdb_90.csv"
else:
    output_filename = "network_tem1_msa_90.csv"

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
print("Number of contacts with conservation score >= 0.99: ", counter_99)

with open(output_filename, "w", newline="") as csvfile:
    csv_writer = csv.DictWriter(csvfile, fieldnames=conservation_tem_msa.keys())
    csv_writer.writeheader()
    csv_writer.writerow(conservation_tem_msa)

if contact_index == "pdb":
    with open(colors_file, "w", newline="") as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=colors_int_type.keys())
        csv_writer.writeheader()
        csv_writer.writerow(colors_int_type)
