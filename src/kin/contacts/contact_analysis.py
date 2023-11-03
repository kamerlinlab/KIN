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

from multiprocessing import Pool
import numpy as np
import pandas as pd
from MDAnalysis import Universe
from MDAnalysis.analysis import distances

from kin.contacts.salt_bridges import (
    check_for_salt_bridge,
    check_for_c_term_salt_bridge,
)
from kin.contacts.hbonds import check_for_hbond
from kin.contacts.cation_pi import check_for_cation_pi
from kin.contacts.pi_pi import check_for_pi_pi
from kin.contacts.hydrophobic import check_for_hydrophobic
from kin.contacts.van_der_waals import check_for_vdw_interaction

# Used to prefilter residue pairs.
MAX_CA_DIST = 20
MAX_HEAVY_DIST = 6  # High so can still find pi-pi interactions.


def single_frame_contact_analysis(
    out_file: str,
    coordinates_file: str,
    topology_file: Optional[str] = None,
    first_res: Optional[int] = None,
    last_res: Optional[int] = None,
    report_time_taken: bool = True,
) -> list[str]:
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
    list[str]
        Each item is a string describing a contact identified.
        Formatting is as follows:
        [residue 1] [residue 2] [interaction type] [part(s) of residue involved]
    """
    if report_time_taken:
        start_time = time.monotonic()

    universe, start_res, final_res = _prep_system(
        coords_file=coordinates_file,
        topology_file=topology_file,
        first_res=first_res,
        last_res=last_res,
    )

    res_pairs = _pre_filter_res_pairs(
        start_res=start_res, final_res=final_res, universe=universe
    )

    print("Sytem setup complete, identifying interactions now.")

    # identify all contacts in the frame.
    contacts_found = _process_single_frame(universe=universe, res_pairs=res_pairs)

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
    trajectory_file: str,
    topology_file: Optional[str] = None,
    first_res: Optional[int] = None,
    last_res: Optional[int] = None,
    num_processes: Optional[int] = None,
    report_time_taken: bool = True,
) -> pd.DataFrame:
    """
    Identify all contacts present in a trajectory file.
    If you have only a single frame to analyse,
    use the function: "single_frame_contact_analysis" instead.

    Parameters
    ----------
    out_file: str
        File path to write the results to.

    coordinates_file: str,
        File path to the trajectory_file.
        Needs to be a file type supported by MDAnalysis (most standard).

    topology_file: Optional[str]
        Depending on the file type of the trajectory, this may not be required.
        For example if using a pdb file as the coordinates_file.

    first_res: Optional[int]
        First residue to analyse.
        Can be useful if you want to break the analysis into blocks and combine later.
        If not provided, the first residue in the trajectory will be used.

    last_res: Optional[int]
        Last residue to analyse
        Can be useful if you want to break the analysis into blocks and combine later.
        If not provided, the last residue in the trajectory will be used.

    num_processes: Optional[int] = None
        Frames are analysed in parallel by default. You can optionally define how many frames
        to analyse in parallel with this parameter. If not provided (recommended), the
        code will use as many parallel processes as you have cores. You most likely
        only need to play with this parameter if you are getting out of memory issues.

    report_time_taken: bool
        Choose whether to print to the console how long the calculation took to run.
        Optional, default is True.

    Returns
    -------
    pd.DataFrame
        Pandas dataframe with each column a different contact identified.
        Each row is a frame in the trajectory and has a value of either 1 or 0
        depending on whether the contact was observed in the specific frame (1=yes) or not.
    """
    if report_time_taken:
        start_time = time.monotonic()

    universe, start_res, final_res = _prep_system(
        coords_file=trajectory_file,
        topology_file=topology_file,
        first_res=first_res,
        last_res=last_res,
    )

    print("Sytem setup complete, identifying interactions now.")

    # generate tuple of everything needed to run in parralel.
    trajectory_steps = []
    for frame in range(0, len(universe.trajectory)):
        trajectory_steps.append((start_res, final_res, frame, universe))

    all_interactions = []
    with Pool(processes=num_processes) as pool:
        results = pool.imap(_pooling_function, iterable=trajectory_steps)

        for per_frame_results in results:
            all_interactions.append(per_frame_results)

    if report_time_taken:
        end_time = time.monotonic()
        delta_time = timedelta(seconds=end_time - start_time)
        print(f"Time taken: {delta_time}")

    results_df = _format_multi_frame_results(all_interactions)
    results_df.to_csv(out_file, index=False)
    return results_df


def _pooling_function(args: tuple[int, int, int, Universe]) -> list[str]:
    """
    Pooling function used in multiframe analysis. Enables analysis of multiple
    trajectory frames at once.

    Parameters
    ----------
    args: tuple[int, int, int, Universe]
        The arguments needed for each seperate process run using multiprocessing.
        This requires 4 items provided as a tuple:
        start_res, final_res, timestep, universe.

    Returns
    -------
    list[str]
        Each item is a string describing a contact identified.
        Formatting is as follows:
        [residue 1] [residue 2] [interaction type] [part(s) of residue involved]
    """
    start_res, final_res, timestep, universe = args
    universe.trajectory[timestep]  # set the universe to the correct timestep.

    res_pairs = _pre_filter_res_pairs(
        start_res=start_res, final_res=final_res, universe=universe
    )
    per_frame_results = _process_single_frame(universe=universe, res_pairs=res_pairs)

    return per_frame_results


def _process_single_frame(
    universe: Universe, res_pairs: list[tuple[int, int]]
) -> list[str]:
    """
    The main logic to analyse a single structure/frame.

    Parameters
    ----------
    universe: Universe
        MDAnalysis universe object.

    res_pairs: list[tuple[int, int]]
        list of residue pairs to analyse.

    Returns
    -------
    list[str]
        Each item is a string describing a contact identified.
        Formatting is as follows:
        [residue 1] [residue 2] [interaction type] [part(s) of residue involved]
    """
    c_term_res_numbs = list(universe.select_atoms("name OXT").resids)
    interactions_found = []
    for res1, res2 in res_pairs:
        # keeps track of interactions found for current residue pair and timestep.
        found_interactions = {
            "mc-mc": False,
            "sc-mc": False,
            "mc-sc": False,
            "sc-sc": False,
        }

        # Now begin searching for interactions.
        result = check_for_salt_bridge(res_numbers=(res1, res2), universe=universe)
        if result:
            found_interactions["sc-sc"] = True
            interactions_found.append(result)

        if (res1 in c_term_res_numbs) or (res2 in c_term_res_numbs):
            result = check_for_c_term_salt_bridge(
                res_numbers=(res1, res2),
                c_term_res_numbs=c_term_res_numbs,
                universe=universe,
            )
            if result:
                interaction_type = result.split(" ")[3]  # mc-sc or sc-mc possible.
                found_interactions[interaction_type] = True
                interactions_found.append(result)

        results = check_for_hbond(res_numbers=(res1, res2), universe=universe)
        if results:
            # unlike other contats, hbond results are a list as more than 1 possible per pair.
            for result in results:
                interaction_type = result.split(" ")[3]

                if found_interactions[interaction_type]:
                    continue  # already a saltbridge describing this.

                interactions_found.append(result)
                found_interactions[interaction_type] = True

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

        if not found_interactions["sc-sc"]:
            result = check_for_hydrophobic(res_numbers=(res1, res2), universe=universe)
            if result:
                found_interactions["sc-sc"] = True
                interactions_found.append(result)

        if abs(res1 - res2) <= 3:
            continue  # residues too close in sequence to be interesting...

        if any(list(found_interactions.values())):
            continue  # no vdw_check required if any other type of interaction found.

        result = check_for_vdw_interaction(res_numbers=(res1, res2), universe=universe)
        if result:
            interactions_found.append(result)

    return interactions_found


def _prep_system(
    coords_file: str,
    topology_file: Optional[str] = None,
    first_res: Optional[int] = None,
    last_res: Optional[int] = None,
) -> tuple[Universe, int, int]:
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

    if start_res >= final_res:
        raise ValueError(
            f"""Your current selection of first_res and last_res would give you no results.
            Revise them and re-run the command.
            The last residue I found in your protein has residue number:{max(ca_atoms.resids)} """
        )

    return universe, start_res, final_res


def _pre_filter_res_pairs(
    start_res: int, final_res: int, universe: Universe
) -> list[tuple[int, int]]:
    """
    Pre filter all possible residue pairs using the heavy atom distances.
    This helps massively reduce the number of potential interacting pairs to investigate.
    Particularly useful for a large system.

    Parameters
    ----------
    start_res: int
        first residue to analyse.

    final_res: int
        final residue to analyse

    universe: Universe
        MDAnalysis universe object.

    Returns
    -------
    list[tuple[int, int]]
        List of residue pairs whose contacts should be analysed.
    """
    ca_atoms = universe.select_atoms("name CA")
    biggest_res = max(ca_atoms.resids)

    all_heavy_atoms_sele = "not name H* and resid 1" + "-" + str(biggest_res)
    all_heavy_atoms = universe.select_atoms(all_heavy_atoms_sele)

    # determine which residue each heavy atom belongs to.
    residue_ranges = {}
    for res_numb in range(1, biggest_res + 1):
        residue_range = np.where(all_heavy_atoms.atoms.resids == res_numb)
        residue_ranges[res_numb] = residue_range

    heavy_atom_dists = distances.distance_array(
        all_heavy_atoms.positions,
        all_heavy_atoms.positions,
    )

    res_pairs = []
    for res1 in range(start_res, final_res + 1):
        res_dists = heavy_atom_dists[residue_ranges[res1]]

        for res2 in range(res1 + 1, biggest_res + 1):
            res_res_dists = res_dists[:, residue_ranges[res2]]

            if res_res_dists.min() <= MAX_HEAVY_DIST:
                res_pairs.append((res1, res2))

    return res_pairs


def _format_multi_frame_results(all_interactions: list[list[str]]) -> pd.DataFrame:
    """
    Given a list of results from the single frame analysis, produce a dataframe with
    columns each unique interaction, and their occupancy (1 or 0).

    Parameters
    ----------
    all_interactions: list[ list[str] ]
        List of all interactions identified across a trajectory.
        Outer list is the trajectory frame.
        Inner list is of the interactions found for that frame.

    Returns
    -------
    pd.DataFrame
        Dataframe with columns being each unique interaction.
        Rows correspond to each frame in the trajectory,
        with 1 = interaction present, 0 = not present.
    """
    unique_interactions = []
    for frame in all_interactions:
        for interaction in frame:
            if interaction in unique_interactions:
                continue
            else:
                unique_interactions.append(interaction)

    # Initialise an empty dictionary for each interaction.
    # Per frame results (present - 1, or not - 0) will be added here.
    per_frame_results = {}
    for interaction in unique_interactions:
        per_frame_results[interaction] = []

    for frame in all_interactions:
        for interaction in unique_interactions:
            if interaction in frame:
                per_frame_results[interaction].append(1)
            else:
                per_frame_results[interaction].append(0)

    return pd.DataFrame(per_frame_results)
