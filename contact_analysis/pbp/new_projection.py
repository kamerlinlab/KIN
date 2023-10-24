from re import L
from tools_proj.pymol_projections import project_pymol_res_res_scores as pyml
import numpy as np
import pandas as pd
from tools_proj import msa_network as toolsnet

# Load data
network_nv_1 = toolsnet.get_contacts_from_csv("network_1nrf_pdb_nv.csv")
colors_nv_1 = toolsnet.get_contacts_from_csv("colors_1nrf_pdb_nv.csv", value_type=str)
network_nv_2 = toolsnet.get_contacts_from_csv("no_2olu/network_1nrf_pdb_nv.csv")
colors_nv_2 = toolsnet.get_contacts_from_csv(
    "no_2olu/colors_1nrf_pdb_nv.csv", value_type=str
)
network_nv_3 = toolsnet.get_contacts_from_csv("1nrf_1hd8_1tvf/network_1nrf_pdb_nv.csv")
colors_nv_3 = toolsnet.get_contacts_from_csv(
    "1nrf_1hd8_1tvf/colors_1nrf_pdb_nv.csv", value_type=str
)

all_nets = [network_nv_1, network_nv_2, network_nv_3]
all_colors = [colors_nv_1, colors_nv_2, colors_nv_3]
counter = 0
for indx, i in enumerate(all_nets):
    network_50 = {}
    colors_50 = {}
    network_90 = {}
    colors_90 = {}
    network_nv = all_nets[indx]
    colors_nv = all_colors[indx]
    counter += 1
    for key, value in network_nv.items():
        if value >= 0.5:
            network_50[key] = np.array(value)
            colors_50[key] = colors_nv[key]
        if value >= 0.9:
            network_90[key] = np.array(value)
            colors_90[key] = colors_nv[key]
    if len(network_50) > 0:
        pyml(network_50, f"network_50_{counter}.pml", colors_50)
    if len(network_90) > 0:
        pyml(network_90, f"network_90_{counter}.pml", colors_90)

    # Get the projection
net1_grid = toolsnet.make_grid(network_nv_1, 263)
toolsnet.plot_int_map(net1_grid, "PBP projected on 1NRF")
net2_grid = toolsnet.make_grid(network_nv_2, 263)
toolsnet.plot_int_map(net2_grid, "PBP projected on 1NRF")
net3_grid = toolsnet.make_grid(network_nv_3, 263)
toolsnet.plot_int_map(net3_grid, "PBP projected on 1NRF")
