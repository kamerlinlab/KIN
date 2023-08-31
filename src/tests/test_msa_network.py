"""This file takes in contacts updated with the msa indexing,
and outputs a network of contacts shared among all the structures
along with their conservation scores. """

from itertools import chain
from collections import Counter
import glob
import os
import numpy as np
import pandas as pd
import time
from tools_proj.pymol_projections import project_pymol_res_res_scores

from tools_proj.msa_network import common_network


input_fiels = (
    "/Users/dariiayehorova/lk_research/tools-project/src/tests/data/contact_msa_files"
)
projection_output = "/Users/dariiayehorova/lk_research/tools-project/src/tests/data/1M40_TEM-1_test_network.pml"

conservation_tem_msa, colors_int_type = common_network(
    input_fiels, "1M40_TEM-1", contact_index="pdb", no_vdw=True, only_sc=False
)
project_pymol_res_res_scores(conservation_tem_msa, projection_output, colors_int_type)
