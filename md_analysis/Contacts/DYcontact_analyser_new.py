import DY_contact_identification as contact_identification

TOPOLOGY_FILE = "/storage/home/hhive1/dyehorova3/data/tools/Simulation_runs/sys_7QLP_TEM-171/clean_all_runs/clean.7QLP_TEM-171_apo.prmtop"
TRAJECTORY_FILE = "/storage/home/hhive1/dyehorova3/data/tools/Simulation_runs/sys_7QLP_TEM-171/clean_all_runs/first_frame.nc"

SEQUENCE_FILE = "7QLP_TEM-171_apo_postleap.seq"
MSA_SEQUENCES_FILE = "bettaLac.ali"
PROTEIN_NAME = "7QLP_TEM-171"


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
    "A": "Ala",
    "R": "Arg",
    "D": "Asp",
    "N": "Asn",
    "C": "Cys",
    "E": "Glu",
    "Q": "Gln",
    "G": "Gly",
    "H": "His",
    "I": "Ile",
    "L": "Leu",
    "K": "Lys",
    "M": "Met",
    "F": "Phe",
    "P": "Pro",
    "S": "Ser",
    "T": "Thr",
    "W": "Trp",
    "Y": "Tyr",
    "V": "Val",
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
    out_file="7QLP_TEM-171_msa_ind_contacts.pickle",
    report_timings=True,  # optional
)
