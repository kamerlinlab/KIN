"""
Tests for sequences module. 
"""

from pathlib import Path
import kin.contacts as contact_analysis
from kin.sequences import seq_align_file_to_sequences


# location of data.
CONTACTS_FILE_LOCATION = Path(contact_analysis.__file__)
TEST_DATA_DIR = CONTACTS_FILE_LOCATION.parents[2] / "tests" / "data"

ALINGMENT_FILE = TEST_DATA_DIR / Path("test_msa_file.ali")  # Path("bettaLac.ali")  #


def test_seq_align_file_to_sequences_with_msa_format():
    """Test with output_msa_style set to true"""
    alingments = seq_align_file_to_sequences(
        alignment_file=str(ALINGMENT_FILE), output_msa_style=True
    )
    assert len(alingments) == 3
    for sequence in alingments.values():
        assert len(sequence) == 145

    start_seq = ["L", "N", "Q", "I", "V", "N", "Y", "N", "-", "-"]
    end_seq = ["N", "L", "K", "-", "-", "-", "-", "-", "-", "-", "-"]
    assert start_seq == alingments["1BUE_NmcA"][0:10]
    assert end_seq == alingments["1BUE_NmcA"][-11:]


def test_seq_align_file_to_sequences_not_msa_format():
    """Test with output_msa_style set to false"""
    alingments = seq_align_file_to_sequences(
        alignment_file=str(ALINGMENT_FILE), output_msa_style=False
    )
    assert len(alingments) == 3
    for sequence in alingments.values():
        assert len(sequence) < 145
        assert "-" not in sequence

    start_seq = ["L", "N", "Q", "I", "V", "N", "Y", "N", "T", "R"]
    end_seq = ["E", "A", "S", "R", "I", "A", "I", "D", "N", "L", "K"]
    assert start_seq == alingments["1BUE_NmcA"][0:10]
    assert end_seq == alingments["1BUE_NmcA"][-11:]
