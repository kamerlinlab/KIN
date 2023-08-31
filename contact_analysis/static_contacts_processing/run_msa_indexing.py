"""Converting all the md-based contacts to the msa indexing and counting contacts only if they are 
Present in 50% of the simultion time"""
import os

from tools_proj.msa_indexing import parse_fasta
from tools_proj.msa_indexing import indexing_pdb_to_msa
from tools_proj.msa_indexing import clean_up_sequence
from tools_proj.msa_indexing import parse_contact_output


INPUT_DIRECTORY = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/crystal_contacts"
OUTPUT_DIRECTORY = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/static_contacts_processing/msa_index_contacts"
MSA_SEQ_FILE = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/static_contacts_processing/bettaLac.ali"

sequence_dict = parse_fasta(MSA_SEQ_FILE)

if os.path.isdir(INPUT_DIRECTORY):
    for filename in os.listdir(INPUT_DIRECTORY):
        if filename.endswith(".txt"):
            file_path = os.path.join(INPUT_DIRECTORY, filename)
            SYSTEM_NAME = filename.split(".txt")[0]
            output_file_path = os.path.join(
                OUTPUT_DIRECTORY, f"{SYSTEM_NAME}_msa_crystal.csv"
            )
            print("Processing ", SYSTEM_NAME)
            seq, short_seq = clean_up_sequence(sequence_dict, SYSTEM_NAME)
            pdb_df_md = parse_contact_output(
                file_path, contact_type="crystal", retention_percent=0.5
            )
            msa_df_md = indexing_pdb_to_msa(seq, pdb_df_md)
            msa_df_md.to_csv(output_file_path, index=False)
