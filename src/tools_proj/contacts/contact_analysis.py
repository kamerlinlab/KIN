"""
Provides the user interface to run contact analysis.

This will be the main file to define how the user interacts with the contact module.
TODO: Think about how to make compataible with multi-frame file.
"""
from typing import Optional
import warnings

from MDAnalysis import Universe
from MDAnalysis.analysis import distances

from tools_proj.contacts.salt_bridges import check_for_salt_bridge
# from tools_proj.contacts.hydrogen_bonds import check_for_hydrogen_bond # TODO
from tools_proj.contacts.cation_pi import check_for_cation_pi
from tools_proj.contacts.pi_pi import check_for_pi_pi
# from tools_proj.contacts.hydrophobic import check_for_hydrophobic # TODO
from tools_proj.contacts.van_der_waals import check_for_vdw_interaction


def single_frame_contact_analysis(topology_file:str,
                             trajectory_file:str,
                             out_file: str,
                             first_res: Optional[int] = None,
                             last_res: Optional[int] = None,
                             ):
    """
    Identify all contacts for a single frame/structure.

    TODO: Can we make it possible for user to edit the defaults for a cut-off:e.g. hydrogen bond distance.
    TODO: Should the topology become optional? As PDB only is also possible
    TODO: Complete logic that covers if e.g. a salt bridge is found we don't also report a sc-sc h bond
    """
    # not required for any of the tasts below.
    warnings.filterwarnings("ignore", message="Element information is missing")
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
            if res1 == res2:
                continue

            # If residues CA-CA dist is greater than 20 A, skip.
            ca_dist = ca_dist_matrix[res1-1, res2-1] # 0-indexed
            if ca_dist > 20:
                continue

            # keeps track of interactions found for current residue pair.
            found_interactions = {"mc-mc": False, "sc-mc": False, "mc-sc": False, "sc-sc": False}

            # Now begin searching for interactions.
            result = check_for_salt_bridge(res_numbers=(res1, res2), universe=universe)
            if result:
                found_interactions["sc-sc"] = True
                interactions_found.append(result)

            # result = check_for_hydrogen_bond(res_numbers=(res1, res2), universe=universe)
            # TODO - will be a bit more challegning to define which interactions to find.
            # if result:
            #     interactions_found.append(result)

            if not found_interactions["sc-sc"]:
                result = check_for_cation_pi(res_numbers=(res1, res2), universe=universe)
                if result:
                    found_interactions["sc-sc"] = True
                    interactions_found.append(result)

            if not found_interactions["sc-sc"]:
                result = check_for_pi_pi(res_numbers=(res1, res2), universe=universe)
                if result:
                    found_interactions["sc-sc"] = True
                    interactions_found.append(result)

            # if not found_interactions["sc-sc"]:
            #     result = check_for_hydrophobic(res_numbers=(res1, res2), universe=universe)
            #     if result:
            #         found_interactions["sc-sc"] = True
            #         interactions_found.append(result)

            if abs(res1-res2) <= 3:
                continue # residues too close in sequence to be interesting...

            if any(list(found_interactions.values())):
                continue # no vdw_check required if other type of interaction found.

            result = check_for_vdw_interaction(res_numbers=(res1, res2), universe=universe)
            if result:
                interactions_found.append(result)

    # for now, before final output file format decided upon and standardised etc...
    return interactions_found
