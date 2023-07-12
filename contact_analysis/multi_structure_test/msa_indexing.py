"""Following code adds the msa-based indexing to both residues of each contact"""
import pandas as pd


MSA_SEQUENCES_FILE = "bettaLac.ali"
PROTEIN_NAME = "STRUCTURE"
PDB_OUTPUT = "INPUTPATH/STRUCTURE_test.txt"
MSA_OUTPUT = "STRUCTURE_msa.csv"


def parse_fasta(file_path):
    """Takes in a msa alignment produced by modeller in fasta formating and
    outputs a sequence as string with '-' for the gaps introduced by msa"""
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


def indexing_pdb_to_msa(msa_sequence: list[str], df: pd.DataFrame) -> pd.DataFrame:
    """This funciton takes in the msa sequence and a string of the two columns
    of the output file and returns two new idecies"""

    res1_list = list(df["Res1"])
    res2_list = list(df["Res2"])
    counter = 0.0
    index_pdb_msa = {}
    msa_indx_res1 = []
    msa_indx_res2 = []
    missing_indicies = []

    for i, res in enumerate(msa_sequence):
        if res != "-":
            counter += 1
            index_pdb_msa[int(counter)] = i + 1
        else:
            missing_indicies.append(i + 1)
    print("Missing residues:", missing_indicies)
    for res_counter, res1 in enumerate(res1_list):
        pdb_indx_res1 = res1[3:]
        res2 = res2_list[res_counter]
        pdb_indx_res2 = res2[3:]
        msa_indx_res1.append(index_pdb_msa[int(pdb_indx_res1)])
        msa_indx_res2.append(index_pdb_msa[int(pdb_indx_res2)])

    df["Res1_msa"] = msa_indx_res1
    df["Res2_msa"] = msa_indx_res2
    return df


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


pdb_df = pd.read_csv(PDB_OUTPUT, delimiter=" ")
pdb_df = pdb_df.dropna(axis=1)
msa_df = indexing_pdb_to_msa(sequence, pdb_df)
msa_df.to_csv(MSA_OUTPUT, index=False)
