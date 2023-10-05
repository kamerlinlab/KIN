"""
Various functions to help work with protein sequences
"""


def seq_align_file_to_sequences(
    alignment_file: str, output_msa_style: bool
) -> dict[str, list[str]]:
    """
    Take a sequence alignment file with multiple sequences
    and extract each sequence and the name of the sequence/protein.
    Return each sequence as a dictionrary item.

    Parameters
    ----------
    alignment_file: str
        Path to the alignment file to process.

    output_msa_style: bool
        If True, then sequences returned in msa formatting.
        This means the gaps (i.e., these: "-") are retained in the sequence.
        If False, the gaps are removed, to give just the protein sequence.

    Returns
    ----------
    dict[str, list[str]
        keys of the dictionary are each protein (obtained from the seq alignment file).
        Values are a list of each amino acid (1 letter code) in the sequence.
    """
    seq_alignments = {}
    with open(alignment_file, "r", encoding="utf-8") as file_in:
        current_seq, current_protein = "", ""
        for line in file_in:
            if (line == "\n") or ("sequence" in line):
                continue

            # start of new alingment
            if ">" in line:
                if len(current_seq) != 0:
                    seq_alignments[current_protein] = list(current_seq)

                # reset seq and prot as new sequence starts now.
                current_protein = line.strip().split(">")[1]
                current_seq = ""

            # line containing sequence.
            else:
                msa_seq_part = line.replace("*", "")

                if output_msa_style:
                    current_seq += msa_seq_part.strip()
                else:
                    prot_seq_part = msa_seq_part.strip().replace("-", "")
                    current_seq += prot_seq_part

        # catches the final sequence (as now hit EOF)
        seq_alignments[current_protein] = current_seq

    return seq_alignments
