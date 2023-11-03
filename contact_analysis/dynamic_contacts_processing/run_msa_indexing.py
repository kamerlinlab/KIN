"""Converting all the md-based contacts to the msa indexing and counting contacts only if they are
Present in 50% of the simultion time"""
import os

from kin.msa_indexing import parse_fasta
from kin.msa_indexing import indexing_pdb_to_msa
from kin.msa_indexing import clean_up_sequence
from kin.msa_indexing import parse_contact_output


INPUT_DIRECTORY = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/simulation_contacts"
OUTPUT_DIRECTORY = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/msa_index_contacts/retention_99/"
MSA_SEQ_FILE = "/Users/dariiayehorova/lk_research/tools-project/contact_analysis/dynamic_contacts_processing/bettaLac.ali"

sequence_dict = parse_fasta(MSA_SEQ_FILE)

for subdir in os.listdir(INPUT_DIRECTORY):
    subdir_path = os.path.join(INPUT_DIRECTORY, subdir)
    if os.path.isdir(subdir_path):
        for filename in os.listdir(subdir_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(subdir_path, filename)
                SYSTEM_NAME = filename.split("_all")[0]
                output_file_path = os.path.join(
                    OUTPUT_DIRECTORY, f"{SYSTEM_NAME}_msa_md_99.csv"
                )
                print("Processing ", SYSTEM_NAME)
                seq, short_seq = clean_up_sequence(sequence_dict, SYSTEM_NAME)
                pdb_df_md = parse_contact_output(
                    file_path, contact_type="md", retention_percent=0.99
                )
                msa_df_md = indexing_pdb_to_msa(seq, pdb_df_md)
                msa_df_md.to_csv(output_file_path, index=False)
