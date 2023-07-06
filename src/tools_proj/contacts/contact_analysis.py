"""
Provides the user interface to run contact analysis.

Two functions for direct use:
1. single_frame_contact_analysis()
2. multi_frame_contact_analysis()
With the only difference being if you have a single or multiple files to analyse.

"""
from typing import Optional
import warnings
import time
from datetime import timedelta

import numpy as np
import pandas as pd # will use soon, TODO.
import MDAnalysis
from MDAnalysis import Universe
from MDAnalysis.analysis import distances

from tools_proj.contacts.salt_bridges import check_for_salt_bridge
# from tools_proj.contacts.hydrogen_bonds import check_for_hydrogen_bond # TODO
from tools_proj.contacts.cation_pi import check_for_cation_pi
from tools_proj.contacts.pi_pi import check_for_pi_pi
# from tools_proj.contacts.hydrophobic import check_for_hydrophobic # TODO
from tools_proj.contacts.van_der_waals import check_for_vdw_interaction


def single_frame_contact_analysis(
    out_file: str,
    coordinates_file:str,
    topology_file:Optional[str] = None,
    first_res: Optional[int] = None,
    last_res: Optional[int] = None,
    report_time_taken: bool = True
    ):
    """
    Identify all contacts present in a single structure.
    If you have multiple frames to analyse,
    use the function: "multi_frame_contact_analysis" instead.

    NOTE:
    A topology file is not required for this function to run.
    For example you could just provide a ".pdb" file to the parameter: "coordinates_file".
    That said, certain coordinate file types (e.g. .netcdf, .rst) file require a topolgy to work.

    The topology and trajectory files used should be compataible with MDAnalysis:
    https://docs.mdanalysis.org/1.1.1/documentation_pages/topology/init.html

    Parameters
    ----------
    out_file: str
        File path to write the results to.

    coordinates_file: str,
        File path to the single structure (e.g. .pdb file)
        Should be a file type supported by MDAnalysis

    topology_file: Optional[str]

        Depending on the file type of the trajectory, this may not be required.

    first_res: Optional[int]
        First residue to analyse.
        Can be useful if you want to break the analysis into blocks and combine later.
        If not provided, the first residue in the trajectory will be used.

    last_res: Optional[int]
        Last residue to analyse
        Can be useful if you want to break the analysis into blocks and combine later.
        If not provided, the last residue in the trajectory will be used.

    report_time_taken: bool
        Choose whether to print to the console how long the calculation took to run.
        Optional, default is True.

    Returns
    -------
    TODO

    """
    universe, start_res, final_res, ca_atoms = _prep_system(
        coords_file=coordinates_file,
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


    with open(out_file, "w", encoding="utf-8") as tfile:
        tfile.write("Res1 Res2 Interaction_Type Residue_Parts \n")
        tfile.write("\n".join(contacts_found))
    print(f"Analysis complete, the file {out_file} has been written to disk")

    if report_time_taken:
        end_time = time.monotonic()
        delta_time = timedelta(seconds=end_time - start_time)
        print(f"Time taken: {delta_time}")

    return contacts_found


def multi_frame_contact_analysis(
    out_file: str,
    trajectory_file:str,
    topology_file:Optional[str] = None,
    first_res: Optional[int] = None,
    last_res: Optional[int] = None,
    report_time_taken: bool = True
    ):
    """
    Identify all contacts present in a trajectory file.
    If you have only a single frame to analyse,
    use the function: "single_frame_contact_analysis" instead.


    """
    universe, start_res, final_res, ca_atoms = _prep_system(
        coords_file=trajectory_file,
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
    The main logic to analyse a single structure/frame.

    Parameters
    ----------
    universe: Universe
        MDAnalysis universe object.

    start_res: int
        First residue to analyse.

    final_res: int
        Last residue to analyse

    ca_dist_matrix: np.ndarray
        Distance matrix between all Calpha atoms.
        Matrix size is [Number of residues x number of residues].

    Returns
    -------
    list[str]
        Each item is a string describing a contact identified.
        Formatting is as follows:
        [residue 1] [residue 2] [interaction type] [part(s) of residue involved]
    """
    interactions_found = []
    for res1 in range(start_res, final_res + 1):
        for res2 in range(res1, final_res + 1):

            try:
                ca_ca_dist = ca_dist_matrix[res1-1, res2-1] # 0-indexed
            except IndexError as error:
                ca_atoms = universe.select_atoms("name CA")
                last_res_numb = max(ca_atoms.resids)
                specific_message = f"""
                It seems like you stated you have more residues than you actually have.
                The last residue I found in your input file(s) is: {last_res_numb}.
                Tip, don't provide the parameter "last_res" if you just want to analyse all residues.
                """
                raise RuntimeError(specific_message) from error

            # two quick tests to filter out interactions.
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


def _prep_system(
    coords_file:str,
    topology_file:Optional[str] = None,
    first_res: Optional[int] = None,
    last_res: Optional[int] = None,
) -> tuple[Universe, int, int, MDAnalysis.core.groups.AtomGroup]:
    """
    Handles the setup of single or multi-frame trajectory analysis.

    Parameters
    ----------
    coords_file: str,
        File path to the single or multi-frame coords file.
        Should be a file type supported by MDAnalysis

    topology_file: Optional[str]
        Depending on the file type of the coords_file, this may not be required.

    first_res: Optional[int]
        First residue to analyse.
        If not provided, the first residue in the trajectory will be used.

    last_res: Optional[int]
        Last residue to analyse
        If not provided, the last residue in the trajectory will be used.

    Returns
    -------
    universe: Universe
        MDAnalysis universe object.

    start_res: int
        First residue to analyse.

    final_res: int
        Last residue to analyse

    ca_atoms: MDAnalysis.core.groups.AtomGroup
        MDAnalysis selection of all Calpha atoms present in structure.
    """

    # not required for any of the tasks below.
    warnings.filterwarnings("ignore", message="Element information is missing")

    if topology_file:
        universe = Universe(topology_file, coords_file)
    else:
        universe = Universe(coords_file)

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


# def format_multi_frame_results(all_interactions: list[list]) -> pd.DataFrame:
#     """
#     Given a list of results from the single frame analysis, produce a dataframe with
#     columns each unique interaction, and their occupancy (1 or 0).


#     TODO - optional param to merge at residue level? - or seperate function?

#     """



#     return "hello"
