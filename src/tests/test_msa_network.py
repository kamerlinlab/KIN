"""This file takes in contacts updated with the msa indexing,
and outputs a network of contacts shared among all the structures
along with their conservation scores. """

from tools_proj.pymol_projections import project_pymol_res_res_scores

from tools_proj.msa_network import common_network


input_fiels = (
    "/Users/dariiayehorova/lk_research/tools-project/src/tests/data/contact_msa_files"
)
projection_output = "/Users/dariiayehorova/lk_research/tools-project/src/tests/data/1M40_TEM-1_test_network.pml"
missing_contacts_output = "/Users/dariiayehorova/lk_research/tools-project/src/tests/data/1M40_TEM-1_missing_network.pml"
# Missing network is always returned as a variable, but if the user does not want it, it is assigned to a dummy variable
(
    conservation_tem_msa,
    colors_int_type,
    missing_contacts,
    missing_colors,
    missing_props,
) = common_network(
    input_fiels,
    "1M40_TEM-1",
    network_index="pdb",
    missing_network=True,
    no_vdw=True,
    only_sc=False,
)
project_pymol_res_res_scores(conservation_tem_msa, projection_output, colors_int_type)
project_pymol_res_res_scores(missing_contacts, missing_contacts_output, missing_colors)
