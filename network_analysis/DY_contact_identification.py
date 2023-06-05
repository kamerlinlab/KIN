from typing import Tuple, Optional, List
import warnings
import pickle
import pandas as pd
import numpy as np
import builtins

import MDAnalysis
from MDAnalysis import Universe
from MDAnalysis.analysis.hydrogenbonds.hbond_analysis import HydrogenBondAnalysis as HBA
from MDAnalysis.analysis import contacts

POSITIVE_SB_RESIDUES = ("LYS", "ARG")
NEGATIVE_SB_RESIDUES = ("GLU", "ASP")
HYDROPHOBIC_RESIDUES = ("ALA", "VAL", "LEU", "ILE", "PRO", "PHE", "Cys")


def calculate_contacts(parm_file: str, traj_file: str, msa_sequence: str,
		short_msa_sequence:str, out_file: str,first_res: Optional[int] = None,
		last_res: Optional[int] = None,
		report_timings: bool = True) -> None:

	if report_timings:
		import time
		from datetime import timedelta
		start_time = time.monotonic()
	
	
	universe = Universe(parm_file, traj_file)
	all_contact_scores = {}
	for res in universe.residues:
		res_name = str(res.resid) + "_" + res.resname.capitalize()
		all_contact_scores[res_name]={}
	
	if first_res is None:
		first_res = 1
	if last_res is None:
		last_res = len(universe.atoms.residues)
		
	for res1 in range(first_res, last_res + 1):
		res1_sele = "not name H* and resid " + str(res1)
		res1_atoms = universe.select_atoms(res1_sele)

        # symmetrical matrix along diagonal, hence loop style.
		for res2 in range(res1, len(universe.residues) + 1):
			res_delta = abs(res1 - res2)
			
			res2_sele = "not name H* and resid " + str(res2)
			res2_atoms = universe.select_atoms(res2_sele)
			contact_scores = []
			for timestep in universe.trajectory:
				res_res_dists = contacts.distance_array(
						res1_atoms.positions,
						res2_atoms.positions)
				contact_score = _score_residue_contact(
						res_res_dists=res_res_dists)
				contact_scores.append(contact_score)
			avg_contact_score = sum(
					contact_scores) / len(universe.trajectory)

			if avg_contact_score > 0.6:
				final_contact_score=1
			else:
				final_contact_score=0

			res1_name = universe.residues[res1-1].resname.capitalize()
			res2_name = universe.residues[res2-1].resname.capitalize()
			contact1_label = str(res1) + "_" + res1_name
			contact2_label = str(res2) + "_" + res2_name 
			all_contact_scores[contact1_label][contact2_label]=final_contact_score
	print("done making contact scores, moved on to indexing")


	msa_contact_scores = indexing_pdb_to_msa(msa_sequence, all_contact_scores)

	#checking the msa to pdb inde conversion
	index_contact_scores = {} 
	for key_1, value_1 in all_contact_scores.items():
		res_pdb_id_1, res_pdb_name_1 = key_1.split("_")
		index_contact_scores[int(res_pdb_id_1)]={}
		for key_2, value_2 in all_contact_scores[key_1].items():
			res_pdb_id_2, res_pdb_name_2 = key_2.split("_")
			index_contact_scores[int(res_pdb_id_1)][int(res_pdb_id_2)]=value_2
		
	pdb_contact_scores = indexing_msa_to_pdb(msa_sequence, msa_contact_scores)

	if pdb_contact_scores == index_contact_scores:
		print("dictionaries are the same")
	else: 
		print("dictionaries are different")

	#save output 
	with open(f"{out_file}", "wb") as file:
		pickle.dump(msa_contact_scores, file)


	if report_timings:
		end_time = time.monotonic()
		delta_time = timedelta(seconds=end_time - start_time)
		print(f"Time taken: {delta_time}")


	
def indexing_pdb_to_msa(msa_sequence: list[str],
		all_contact_scores: dict[str, dict[str,float]]) -> dict[float, float]:
	
	counter=0.0
	index_pdb_msa={}
	msa_contact_scores={}
	missing_indicies = []
	for i, res in enumerate(msa_sequence):
		if res !='-':
			counter+=1
			index_pdb_msa[int(counter)]=i+1
		else:
			missing_msa_indx = i
			missing_indicies.append(i+1)
	print("Missing residues:", missing_indicies)
	for key_1, value_1 in all_contact_scores.items():
		res_pdb_id_1, res_pdb_name_1 = key_1.split("_")
		
		res_msa_id_1 = index_pdb_msa[int(res_pdb_id_1)]
		msa_contact_scores[res_msa_id_1]={}
		for key_2, value_2 in all_contact_scores[key_1].items():
			res_pdb_id_2, res_pdb_name_2 = key_2.split("_")
			res_msa_id_2 = index_pdb_msa[int(res_pdb_id_2)]
			msa_contact_scores[res_msa_id_1][res_msa_id_2]=value_2
			
	return msa_contact_scores

def indexing_msa_to_pdb(msa_sequence: list[str],
		msa_contact_scores: dict[int, dict[int,float]]) -> dict[float, float]:
	
	counter=0
	index_pdb_msa={}
	for i, res in enumerate(msa_sequence):
		if res !='-':
			counter+=1
			index_pdb_msa[i+1]=int(counter)
		else:
			index_pdb_msa[i+1] = "-"
	pdb_contact_scores={}	
	for key_1, value_1 in msa_contact_scores.items():
		res_pdb_id_1 = int(index_pdb_msa[key_1])
		pdb_contact_scores[res_pdb_id_1]={}
		for key_2, value_2 in msa_contact_scores[key_1].items():
			res_pdb_id_2 = int(index_pdb_msa[key_2])
			pdb_contact_scores[res_pdb_id_1][res_pdb_id_2]=value_2
	return pdb_contact_scores

def _atom_num_to_res_info(atom_num: int,
                          universe: MDAnalysis.core.universe.Universe) -> Tuple[str, int]:
    """
    From an MDAnalysis atom number and universe, obtain the residue number
    and residue name.

    Parameters
    ----------
    atom_num: int
        Atom id to get residue info from.

    universe: MDAnalysis.core.universe.Universe
        MDAnalysis universe object

    Returns
    -------
    Tuple[str, int]
        string is resname, int is the resid.
    """
    atom_num = int(atom_num)  # in case float passed.
    donor_info = str(universe.atoms[atom_num].residue)
    donor_parts = donor_info.replace(", ", " ").replace(">", "").split(" ")

    res_name, resid = donor_parts[1], int(donor_parts[2])
    return res_name, resid



def _score_residue_contact(res_res_dists: np.ndarray, dist_cut: float = 6.0) -> float:
    """
    Score the "strength" of a pair of residues based on their atomic distances.
    Same implementation as in pycontact: https://github.com/maxscheurer/pycontact

    Parameters
    ----------
    res_res_dists: np.ndarray[float]
        Distance matrix of size:
        number of atoms in residue 1 x number of atoms in residue 2.

    dist_cut: float=6.0
        Max distance before atom-atom contact not included in scoring.
        Values much larger don't notably affect the score.

    Returns
    -------
    float
        Calculated contact score.
    """
    # question: should i count any distance that passes min cutoff
    # as an interaction?
# Just set it to at least one distance be within the distance 
#Force field per residue interaction 
 

    interactions = 0
    interaction_counter = 0
    for dist in res_res_dists.flatten():
	    if dist < dist_cut: 
		    interactions += dist
		    interaction_counter += 1
    if interaction_counter > 0:
	    avg_interactions = interactions/interaction_counter
    else:
	    avg_interactions = 0
    if avg_interactions != 0:
	    return 1
    else:
	    return 0

