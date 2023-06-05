The final output of the analysis is structured as a disctionary where
each key is a number of a residue based on the global (msa) indexing and
each value is a list of N integeres, where N is a number of sturctures
analyzed and each integer represents a number of interactions formed by
that structure. 
This information is saved in int_in_all_struct.pickle and int_in_all_struct.csv

Additionally there are .csv files for each structre that contain
individual contacts for each stcuture. Specificaly they are structured
as a dictionary of residue indexed by global (msa) indexing, where
corresponding values are dictionories, where the keys are all other
residues present and a value is whether there is an interacction between
the two structures or not. This dictionaries can be converted between
inecies using indexing_pdb_to_msa() and indexing_msa_to_pdb() functions in 
DY_contact_identification.py file.

All files to run multi_kif_dict.py 
are provided so feel free to modify these files as you would see fit. 
