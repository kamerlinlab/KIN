"""
These would be better submitted as jobs, for the first one give maybe 24 hours
and access to a single node, just to see how long it takes and the others can be adjusted from there.

"""
#from key_interactions_finder import contact_identification
import DY_contact_identification as contact_identification
import numpy as np
import csv
import pandas as pd
TOPOLOGY_FILE = "/storage/home/hhive1/dyehorova3/data/tools/Md_processing/Trajectories/sys_SEQ_NAME/no_int_type/SEQ_NAME_apo.prmtop"

TRAJECTORY_FILE = "/storage/home/hhive1/dyehorova3/data/tools/Md_processing/Trajectories/sys_SEQ_NAME/no_int_type/first_frame.nc"

SEQUENCE_FILE = "SEQ_NAME_apo_postleap.seq"
MSA_SEQUENCES_FILE = "pos_ranking_nostar.dat"
SEQUENCE_NAME = 'PDB_NAME'
	
data = (np.genfromtxt(MSA_SEQUENCES_FILE, names=True, dtype=None, encoding=None))
column_sequence = data[SEQUENCE_NAME]
raw_msa_sequence = ''.join(column_sequence)
print("raw", raw_msa_sequence)

residue_map = {
		'A':'Ala', 
		'R':'Arg', 
		'D':'Asp',
		'N':'Asn',
		'C':'Cys', 
		'E':'Glu',
		'Q':'Gln',
		'G':'Gly',
		'H':'His',
		'I':'Ile',
		'L':'Leu',
		'K':'Lys',
		'M':'Met',
		'F':'Phe', 
		'P':'Pro',
		'S':'Ser',
		'T':'Thr',
		'W':'Trp',
		'Y':'Tyr',
		'V':'Val',
		'-':'-'}
short_sequence = raw_msa_sequence.replace("-","")
short_sequence_list =list(short_sequence)
sequence_list = list(raw_msa_sequence)
sequence = [
		residue_map[res] 
		for res in sequence_list]
short_sequence = [
		residue_map[res] 
		for res in short_sequence_list]

contact_identification.calculate_contacts(
		parm_file=TOPOLOGY_FILE,
		traj_file=TRAJECTORY_FILE,
		msa_sequence=sequence,
		short_msa_sequence=short_sequence,
		out_file="SEQ_NAME_msa_ind_contacts.pickle",
		report_timings=True  # optional
		)
