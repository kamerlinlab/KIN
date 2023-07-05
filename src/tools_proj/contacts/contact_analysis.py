"""
Provides the user interface to run contact analysis.

This will be the main file to define how the user interacts with the contact module
"""
from typing import Optional
from MDAnalysis import Universe
from MDAnalysis.analysis import distances

from tools_proj.contacts.salt_bridges import check_for_salt_bridge
# from tools_proj.contacts.hydrogen_bonds import check_for_hydrogen_bond
from tools_proj.contacts.cation_pi import check_for_cation_pi

# TODO - make sure all of these are included in the package.
ALLOWED_RESIDUES = ["ALA", "ARG", "ASN", "ASP", "ASH", "CYS", "CYM", "CYX",
                      "GLU", "GLH", "GLN", "GLY", "HID", "HIE", "HIP", "ILE",
                      "LEU", "LYS", "LYN", "MET", "PHE", "PRO", "SER", "THR",
                      "TRP", "TYR", "VAL"]

def single_frame_contact_analysis(topology_file:str,
                             trajectory_file:str,
                             out_file: str,
                             first_res: Optional[int] = None,
                             last_res: Optional[int] = None,
                             ):
    """
    Identify contact for a single frame/structure.

    Considerations: Can we make it possible for user to edit the defaults for a cut-off:
    e.g. hydrogen bond distance.

    TODO: Should the topology become optional? As PDB only is possible
    TODO: Check if res1/res2 are known residues and if not skip them (can add as a warning to output optionally).

    TODO: If salt bridge found, then side chain h-bond should be skipped etc...
    Need to add the logic to ensure that sort of thing happens. Could be a dict that stores and checks
    if following tests, should be skipped?

    """
    universe = Universe(topology_file, trajectory_file)

    if first_res is None:
        first_res = 1
    if last_res is None:
        last_res = len(universe.atoms.residues)

    # important that this calculation is done on all residues so matrix indexing matches up.
    ca_atoms = universe.select_atoms(f"name CA and resid 1-{len(universe.atoms.residues)}")
    ca_dist_matrix = distances.distance_array(ca_atoms, ca_atoms, box=universe.dimensions)

    print("Setup complete, identifying interactions now.")

    interactions_found = []
    for res1 in range(first_res, last_res + 1):
        for res2 in range(res1, len(universe.residues) + 1):

            # If residues CA-CA dist is greater than 20 A, skip.
            ca_dist = ca_dist_matrix[res1-1, res2-1] # 0-indexed
            if ca_dist > 20:
                continue

            # Now begin searching for interactions.
            result = check_for_salt_bridge(res_numbers=(res1, res2), universe=universe)
            if result:
                interactions_found.append(result)

            # result = check_for_hydrogen_bond(res_numbers=(res1, res2), universe=universe)
            # if result:
            #     interactions_found.append(result)

            result = check_for_cation_pi(res_numbers=(res1, res2), universe=universe)
            if result:
                interactions_found.append(result)

            # result = check_for_pi_pi(res_numbers=(res1, res2), universe=universe)
            # if result:
            #     interactions_found.append(result)

            # might be worthwhile at this point to add something like this?
            # if abs(res1-res2) <= 2:
            #   continue # residues in too close contact, so skipping below tests.

            # result = check_for_hydrophobic(res_numbers=(res1, res2), universe=universe)
            # if result:
            #     interactions_found.append(result)

            # result = check_for_van_der_waals(res_numbers=(res1, res2), universe=universe)
            # if result:
            #     interactions_found.append(result)

    # for now, before final output file format decided upon and standardised etc...
    print(interactions_found)