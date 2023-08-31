"""This file takes in contacts updated with the msa indexing,
and outputs a network of contacts shared among all the structures
along with their conservation scores. """

import csv 
from tools_proj.pymol_projections import project_pymol_res_res_scores
from tools_proj.msa_network import common_network


input_fiels = (
    "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/msa_index_contacts/"
)
projection_output = "1M40_TEM-1_network.pml"
contact_index="pdb"

conservation_tem_msa, colors_int_type = common_network(
    input_fiels, "1M40_TEM-1", contact_index, no_vdw=True, only_sc=False
)
if contact_index == "pdb":
    project_pymol_res_res_scores(conservation_tem_msa, projection_output, colors_int_type)
    output_filename = 'network_tem1_pdb.csv'
else:
    output_filename = 'network_tem1_msa.csv'

with open(output_filename, 'w', newline='') as csvfile:
    csv_writer = csv.DictWriter(csvfile, fieldnames=conservation_tem_msa.keys())
    csv_writer.writeheader()
    csv_writer.writerow(conservation_tem_msa)

