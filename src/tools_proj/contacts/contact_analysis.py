"""
Provides the user interface to run contact analysis.

"""
from typing import Optional
import warnings
import time
from datetime import timedelta

import numpy as np
import pandas as pd
from MDAnalysis import Universe
from MDAnalysis.analysis import distances

from tools_proj.contacts.salt_bridges import check_for_salt_bridge
# from tools_proj.contacts.hydrogen_bonds import check_for_hydrogen_bond # TODO
from tools_proj.contacts.cation_pi import check_for_cation_pi
from tools_proj.contacts.pi_pi import check_for_pi_pi
# from tools_proj.contacts.hydrophobic import check_for_hydrophobic # TODO
from tools_proj.contacts.van_der_waals import check_for_vdw_interaction


def single_frame_contact_analysis(
                             trajectory_file:str,
                             out_file: str,
                             topology_file:Optional[str] = None,
                             first_res: Optional[int] = None,
                             last_res: Optional[int] = None,
                             report_time_taken: bool = True
                             ):
    """
    This
    """
    universe, start_res, final_res, ca_atoms = _prep_system(
        trajectory_file=trajectory_file,
        topology_file=topology_file,
        first_res=first_res,
        last_res=last_res
    )

    if report_time_taken:
        start_time = time.monotonic()

    # important this is done on all atoms so indexing matches up.
    ca_dist_matrix = distances.distance_array(ca_atoms, ca_atoms, box=universe.dimensions)
    print("Sytem setup complete, identifying interactions now.")

    # identify all contacts in the frame.
    contacts_found = _process_single_frame(
        universe=universe,
        start_res=start_res,
        final_res=final_res,
        ca_dist_matrix=ca_dist_matrix)

    if report_time_taken:
        end_time = time.monotonic()
        delta_time = timedelta(seconds=end_time - start_time)
        print(f"Time taken: {delta_time}")

    return contacts_found


def multi_frame_contact_analysis(trajectory_file:str,
                             out_file: str,
                             topology_file:Optional[str] = None,
                             first_res: Optional[int] = None,
                             last_res: Optional[int] = None,
                             report_time_taken: bool = True
                             ):
    """
    TESTING TESTING TESTING...
    """
    universe, start_res, final_res, ca_atoms = _prep_system(
        trajectory_file=trajectory_file,
        topology_file=topology_file,
        first_res=first_res,
        last_res=last_res
    )

    if report_time_taken:
        start_time = time.monotonic()
    print("Setup complete, identifying interactions now.")

    all_interactions = []
    for _ in universe.trajectory: # "_" is the current "timestep"

        # important this is done on all atoms so indexing matches up.
        ca_dist_matrix = distances.distance_array(ca_atoms, ca_atoms, box=universe.dimensions)

        # identify all contacts in the frame.
        per_frame_results = _process_single_frame(
            universe=universe,
            start_res=start_res,
            final_res=final_res,
            ca_dist_matrix=ca_dist_matrix)

        all_interactions.append(per_frame_results)

    if report_time_taken:
        end_time = time.monotonic()
        delta_time = timedelta(seconds=end_time - start_time)
        print(f"Time taken: {delta_time}")

    # TODO - will need to decide how to combine the per frame results.

    # for now, before final output file format decided upon and standardised etc...
    return all_interactions



def _process_single_frame(universe: Universe,
                          start_res: int,
                          final_res: int,
                          ca_dist_matrix:np.ndarray
                          ) -> list[str]:
    """
    Main logic occurs here...

    """
    interactions_found = []
    for res1 in range(start_res, final_res + 1):
        for res2 in range(res1, final_res + 1):

            # two quick tests to filter out interactions.
            ca_ca_dist = ca_dist_matrix[res1-1, res2-1] # 0-indexed
            if (res1 == res2) or ca_ca_dist > 20:
                continue

            # keeps track of interactions found for current residue pair and timestep.
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

    return interactions_found


def _prep_system(trajectory_file:str,
                 topology_file:Optional[str] = None,
                 first_res: Optional[int] = None,
                 last_res: Optional[int] = None,
):
    """
    Handles the setup of single or multi-frame trajectory analysis.

    """

    # not required for any of the tasks below.
    warnings.filterwarnings("ignore", message="Element information is missing")

    if topology_file:
        universe = Universe(topology_file, trajectory_file)
    else:
        universe = Universe(trajectory_file)

    ca_atoms = universe.select_atoms("name CA")
    if first_res is None:
        start_res = min(ca_atoms.resids)
    else:
        start_res = first_res
    if last_res is None:
        final_res = max(ca_atoms.resids)
    else:
        final_res = last_res

    return universe, start_res, final_res, ca_atoms


# def _merge_multi_frame_results(all_interactions: list[list]) -> pd.DataFrame:
#     """
#     Given a list of results from the single frame analysis, produce a dataframe with
#     columns each unique interaction, and their occupancy (1 or 0).


#     TODO - optional param to merge at residue level?

#     """



#     return "hello"