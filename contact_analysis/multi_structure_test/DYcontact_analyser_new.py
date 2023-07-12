import DY_contact_identification as contact_identification

TOPOLOGY_FILE = "SIMPATH/sys_SEQ_NAME/clean_all_runs/clean.SEQ_NAME_apo.prmtop"
TRAJECTORY_FILE = "SIMPATH/sys_SEQ_NAME/clean_all_runs/first_frame.nc"

SEQUENCE_FILE = "SEQ_NAME_apo_postleap.seq"
MSA_SEQUENCES_FILE = "bettaLac.ali"
PROTEIN_NAME = "SEQ_NAME"


def parse_fasta(file_path):
    sequences = {}
    current_name = None
    current_sequence = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()

            if line.startswith(">"):
                if current_name is not None:
                    sequences[current_name] = "".join(current_sequence)
                    current_sequence = []

                current_name = line[1:]
            else:
                current_sequence.append(line)

        # Add the last sequence to the dictionary
        if current_name is not None:
            sequences[current_name] = "".join(current_sequence)

    return sequences


sequence_dict = parse_fasta(MSA_SEQUENCES_FILE)
raw_msa_sequence = sequence_dict.get(PROTEIN_NAME)
residue_map = {
    "A": "ALA",
    "R": "ARG",
    "D": "ASP",
    "N": "ASN",
    "C": "CYS",
    "E": "GLU",
    "Q": "GLN",
    "G": "GLY",
    "H": "HIS",
    "I": "ILE",
    "L": "LEU",
    "K": "LYS",
    "M": "MET",
    "F": "PHE",
    "P": "PRO",
    "S": "SER",
    "T": "THR",
    "W": "TRP",
    "Y": "TYR",
    "V": "VAL",
    "-": "-",
}
raw_msa_sequence = raw_msa_sequence.replace("*", "")
short_sequence = raw_msa_sequence.replace("-", "")

short_sequence_list = list(short_sequence)
sequence_list = list(raw_msa_sequence)
sequence = [residue_map[res] for res in sequence_list]
short_sequence = [residue_map[res] for res in short_sequence_list]


contact_identification.calculate_contacts(
    parm_file=TOPOLOGY_FILE,
    traj_file=TRAJECTORY_FILE,
    msa_sequence=sequence,
    short_msa_sequence=short_sequence,
    out_file="SEQ_NAME_msa_ind_contacts.pickle",
    report_timings=True,  # optional
)
