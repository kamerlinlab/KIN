"""
Simple example of how to use pymol_projections.py

This file can be deleted later.
"""
import pymol_projections

# Initial format is each residue pair stored in a tuple.
res_res_scores = {(1, 5): 2, (1, 7): 0.1, (2, 8): 1.1, (3, 90): 3}
print(f"{res_res_scores=}")

# scale results so max value = 0.5 - good size for pymol cylinder representation.
res_res_scores_scaled = pymol_projections.rescale_scores(
    input_dict=res_res_scores, max_value=0.5
)
print(f"{res_res_scores_scaled=}")

# Outputs the pymol compatable file.
pymol_projections.project_pymol_res_res_scores(
    res_res_scores=res_res_scores_scaled, out_file=r"test_pymol_output.py"
)
