"""
Tests for the utils module
"""
from pathlib import Path
import pytest
import kin.contacts as contact_analysis

from kin.utils import per_residue_distance_to_site, normalise_dict_values

# location of data.
CONTACTS_FILE_LOCATION = Path(contact_analysis.__file__)
TEST_DATA_DIR = CONTACTS_FILE_LOCATION.parents[2] / "tests" / "data"
TEST_FILES = {
    "single_pdb": "4YFM_MAB-1_apo.pdb",
    "single_pdb_with_water": "4YFM_MAB-1_apo_water.pdb",
    "amber_topology": "4YFM_MAB-1_apo.prmtop",
    "amber_inpcrd": "4YFM_MAB-1_apo.inpcrd",
    "amber_traject": "4YFM_MAB-1_test_traj.nc",
    "pdb_traject": "4YFM_MAB-1_test_traj.pdb",
}


per_res_dist_combos = [
    ("resid 1 to 10", 1, 1, {1: 0}),
    ("resid 1 to 5", 1, 5, {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}),
    ("resid 1 and name CA", 1, 1, {1: 0}),
    ("resid 55", 1, 1, {1: 35.76}),
]


@pytest.mark.parametrize("site_def, first, last, expected_result", per_res_dist_combos)
def test_per_residue_distance_to_site(site_def, first, last, expected_result):
    """
    Test the per res distance to site measure gives expected results
    """
    pdb_file_path = str(TEST_DATA_DIR / TEST_FILES["single_pdb"])

    result = per_residue_distance_to_site(
        pdb_file=pdb_file_path,
        site_defintion=site_def,
        first_residue=first,
        last_residue=last,
        side_chain_only=False,
        out_file=None,
    )
    assert result == expected_result


input_dicts = [
    ({1: 14.1, 2: 14, 3: 15}),
    ({1: 0, 2: 14, 3: 18.1}),
    ({1: 10000, 2: 10000, 3: 1}),
]


@pytest.mark.parametrize("input_dict", input_dicts)
def test_normalise_dict_values(input_dict):
    """
    Test function normalise_dict_values does:
    (1) max value is now 1 and
    (2) lowest value equal to or greater than 0.
    (3) The dictionary keys are left alone.
    """
    new_dict = normalise_dict_values(input_dict)
    assert max(new_dict.values()) == pytest.approx(1, 0.01)
    assert 1 > min(new_dict.values()) >= 0


failing_dicts = [
    ({1: "14.1", 2: 14, 3: 15}, TypeError),
    ({}, ValueError),
]


@pytest.mark.parametrize("in_dict, error_type", failing_dicts)
def test_normalise_dict_values_fails(in_dict, error_type):
    """
    Test function normalise_dict_values fails when expected to.
    (1) String given.
    (2) Empty dict given.
    """
    with pytest.raises(error_type):
        _ = normalise_dict_values(in_dict)
