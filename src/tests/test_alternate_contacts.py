"""
Tests for alternate_contacts module. 
"""
import pandas as pd
import pytest

from kin.alternate_contacts import (
    find_equivalent_contacts,
    find_possible_single_point_mutations,
    find_possible_double_mutations,
    _create_pdb_to_msa_converter,
)

### Setup of example data with known behaviour.
EXAMPLE_TARGET_PROT_SEQ = ["A", "G", "V", "L", "R", "G"]
EXAMPLE_TARGET_MSA_SEQ = "-ADARL-GRV"
example_msa_contacts = {
    "target_protein": {
        "Res1_pdb": ["ASP2", "ALA3", "ALA3", "ALA3"],
        "Res2_pdb": ["ARG4", "LEU5", "VAL7", "VAL7"],
        "Res1_msa": [3, 4, 4, 4],
        "Res2_msa": [5, 6, 9, 9],
        "Interaction_Type": ["hbond", "hbond", "vdw", "vdw"],
        "Residue_Parts": ["mc-mc", "mc-mc", "sc-sc", "mc-sc"],
    },
    "other_protein_1": {
        "Res1_pdb": ["ASP2", "ALA3", "ALA3", "ALA3"],
        "Res2_pdb": ["ARG4", "LEU5", "VAL7", "VAL7"],
        "Res1_msa": [3, 4, 4, 4],
        "Res2_msa": [5, 6, 9, 9],
        "Interaction_Type": ["saltbridge", "hbond", "vdw", "vdw"],
        "Residue_Parts": ["mc-mc", "mc-mc", "sc-sc", "mc-sc"],
    },
    "other_protein_2": {
        "Res1_pdb": ["GLU2", "VAL3", "ALA3", "ALA3"],
        "Res2_pdb": ["ARG4", "LEU5", "LEU7", "LEU7"],
        "Res1_msa": [3, 4, 4, 4],
        "Res2_msa": [5, 6, 9, 9],
        "Interaction_Type": ["saltbridge", "hbond", "vdw", "vdw"],
        "Residue_Parts": ["mc-mc", "mc-mc", "sc-sc", "mc-sc"],
    },
}
msa_contacts = {}
for protein, contact_dict in example_msa_contacts.items():
    msa_contacts[protein] = pd.DataFrame(contact_dict)


### tests for function: find_equivalent_contacts
def test_find_equivalent_contacts_without_vdws():
    """Test simple example with vdws interaction not counted."""
    contact_combos, contact_examples = find_equivalent_contacts(
        all_msa_contacs_dfs=msa_contacts,
        target_res_pair=(3, 5),
        target_msa_seq=EXAMPLE_TARGET_MSA_SEQ,
        no_vdws=True,
    )

    expected_contact_combos = {"ALA LEU hbond mc-mc": 2, "VAL LEU hbond mc-mc": 1}
    expected_contact_examples = {
        "ALA LEU hbond mc-mc": [
            ("target_protein", "3", "5"),
            ("other_protein_1", "3", "5"),
        ],
        "VAL LEU hbond mc-mc": [("other_protein_2", "3", "5")],
    }

    assert expected_contact_combos == contact_combos
    assert expected_contact_examples == contact_examples


def test_find_equivalent_contacts_with_vdws():
    """Test simple example with vdws interaction counted."""
    contact_combos, contact_examples = find_equivalent_contacts(
        all_msa_contacs_dfs=msa_contacts,
        target_res_pair=(3, 5),
        target_msa_seq=EXAMPLE_TARGET_MSA_SEQ,
        no_vdws=False,
    )

    expected_contact_combos = {"ALA LEU hbond mc-mc": 2, "VAL LEU hbond mc-mc": 1}
    expected_contact_examples = {
        "ALA LEU hbond mc-mc": [
            ("target_protein", "3", "5"),
            ("other_protein_1", "3", "5"),
        ],
        "VAL LEU hbond mc-mc": [("other_protein_2", "3", "5")],
    }

    assert expected_contact_combos == contact_combos
    assert expected_contact_examples == contact_examples


### tests for function: find_possible_single_point_mutations
test_cases = [
    # gives no result
    ({"ALA LEU hbond mc-mc": 2, "VAL VAL hbond mc-mc": 1}, []),
    # gives 1 result
    (
        {"ALA LEU hbond mc-mc": 2, "VAL LEU hbond mc-mc": 1},
        [{"res_numb": 1, "wt_res": "A", "mutated_res": "V"}],
    ),
    # gives 2 results
    (
        {"ALA LEU hbond mc-mc": 1, "GLY LEU hbond sc-mc": 1, "VAL LEU hbond mc-mc": 1},
        [
            {"res_numb": 1, "wt_res": "A", "mutated_res": "G"},
            {"res_numb": 1, "wt_res": "A", "mutated_res": "V"},
        ],
    ),
]


@pytest.mark.parametrize("contact_combos, expected_result", test_cases)
def test_find_possible_single_point_mutations(contact_combos, expected_result):
    """Test with diff inputs"""
    result = find_possible_single_point_mutations(
        contact_combinations=contact_combos,
        target_res_pair=(1, 4),
        target_prot_seq=EXAMPLE_TARGET_PROT_SEQ,
        conservation_cutoff=0,
    )

    assert result == expected_result


def test_find_possible_single_point_mutations_empty_input():
    """Test with empty input data"""
    result = find_possible_single_point_mutations(
        contact_combinations={},
        target_res_pair=(2, 4),
        target_prot_seq=EXAMPLE_TARGET_PROT_SEQ,
    )
    expected_result = []
    assert result == expected_result


### tests for function: find_possible_double_mutations
test_cases = [
    # gives no results
    (
        {"ALA LEU hbond mc-mc": 2, "VAL LEU hbond mc-mc": 1},
        [],
    ),
    # gives 1 result
    (
        {"ALA LEU hbond mc-mc": 2, "VAL VAL hbond mc-mc": 1},
        [
            {
                "res1_numb": 1,
                "wt_res1": "A",
                "mutated_res1": "V",
                "res2_numb": 4,
                "wt_res2": "L",
                "mutated_res2": "V",
            }
        ],
    ),
]


@pytest.mark.parametrize("contact_combos, expected_result", test_cases)
def test_find_possible_double_mutations(contact_combos, expected_result):
    """Test with diff inputs"""
    result = find_possible_double_mutations(
        contact_combinations=contact_combos,
        target_res_pair=(1, 4),
        target_prot_seq=EXAMPLE_TARGET_PROT_SEQ,
        conservation_cutoff=0,
    )
    assert result == expected_result


def test_find_possible_double_mutations_empty_input():
    """Test with empty input data"""
    result = find_possible_double_mutations(
        contact_combinations={},
        target_res_pair=(2, 4),
        target_prot_seq=EXAMPLE_TARGET_PROT_SEQ,
    )
    expected_result = []
    assert result == expected_result


### tests for function: _create_pdb_to_msa_converter
def test__create_pdb_to_msa_converter():
    """
    Test with a simple MSA sequence
    """
    msa_seq = "AGCDEF"
    expected_result = {
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 5,
        6: 6,
    }
    result = _create_pdb_to_msa_converter(msa_seq)
    assert result == expected_result


def test__create_pdb_to_msa_converter_with_gaps():
    """
    Test with a sequence containing gaps.
    """
    msa_seq = "A-G--CD"
    expected_result = {
        1: 1,
        2: 3,
        3: 6,
        4: 7,
    }
    result = _create_pdb_to_msa_converter(msa_seq)
    assert result == expected_result


def test__create_pdb_to_msa_converter_with_star_at_end():
    """
    Test star at end of seq does not impact results.
    """
    msa_seq_no_star = "AGCF"
    msa_seq_with_star = "AGCF*"

    result_no_star = _create_pdb_to_msa_converter(msa_seq_no_star)
    result_with_star = _create_pdb_to_msa_converter(msa_seq_with_star)

    assert result_no_star == result_with_star


def test__create_pdb_to_msa_converter_empty_sequence():
    """
    Test empty seq returns empty dict.
    """
    msa_seq = ""
    expected_result = {}
    result = _create_pdb_to_msa_converter(msa_seq)
    assert result == expected_result
