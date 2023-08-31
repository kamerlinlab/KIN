"""Following code provides an example of the series of 
command to go from the contacts to the msa indexing"""

from tools_proj.msa_indexing import parse_fasta
from tools_proj.msa_indexing import indexing_pdb_to_msa
from tools_proj.msa_indexing import clean_up_sequence
from tools_proj.msa_indexing import parse_contact_output


MSA_SEQUENCES_FILE = "data/bettaLac.ali"
PROTEIN_NAME = "1M40_TEM-1"
PDB_OUTPUT_STATIC = "data/1M40_TEM-1_test_crystal.txt"
PDB_OUTPUT_DYNAMIC = "data/1M40_TEM-1_test_md.txt"
MSA_OUTPUT_STATIC = "data/1M40_TEM-1_msa_crystal.csv"
MSA_OUTPUT_DYNAMIC = "data/1M40_TEM-1_msa_md.csv"

sequence_dict = parse_fasta(MSA_SEQUENCES_FILE)
seq, short_seq = clean_up_sequence(sequence_dict, PROTEIN_NAME)

# Crystal structure contacts
pdb_df_crystal = parse_contact_output(PDB_OUTPUT_STATIC, contact_type="crystal")
msa_df_crystal = indexing_pdb_to_msa(seq, pdb_df_crystal)
msa_df_crystal.to_csv(MSA_OUTPUT_STATIC, index=False)

# Md data contacts
pdb_df_md = parse_contact_output(PDB_OUTPUT_DYNAMIC, contact_type="md", retention_percent=0.5)
msa_df_md = indexing_pdb_to_msa(seq, pdb_df_md)
msa_df_md.to_csv(MSA_OUTPUT_DYNAMIC, index=False)
