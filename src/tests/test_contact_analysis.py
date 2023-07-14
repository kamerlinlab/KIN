"""
Integration style tests for the contact analyser.

# def test_traject_pdb

# test_traject_topolgy

# test_single_struct

# test_single_frame_blocks
# confirm single frame in blocks give same
# contacts as seperate.

# test_bad_residue_selection
# make sure exits if bad residue selection made.
"""
from pathlib import Path
import tools_proj.contacts as contact_analysis
from tools_proj.contacts.contact_analysis import single_frame_contact_analysis
from tools_proj.contacts.contact_analysis import multi_frame_contact_analysis

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


def test_single_frame_contact_analysis():
    """
    Test analysis on single pdb works and coord and topol work.
    And that they give the same and expected number of contacts.
    """
    pdb_file_path = str(TEST_DATA_DIR / TEST_FILES["single_pdb"])
    result_pdb = single_frame_contact_analysis(
        coordinates_file=pdb_file_path,
        out_file="tmp.tmp",
    )

    coord_file_path = str(TEST_DATA_DIR / TEST_FILES["amber_inpcrd"])
    topology_file_path = str(TEST_DATA_DIR / TEST_FILES["amber_topology"])
    result_topology = single_frame_contact_analysis(
        coordinates_file=coord_file_path,
        topology_file=topology_file_path,
        out_file="tmp.tmp",
    )

    assert len(result_topology) == len(result_pdb)
    assert len(result_pdb) == 739


def test_partial_selection():
    """
    Confirm two smaller selections give the same result as a complete selection
    """
    coord_file_path = str(TEST_DATA_DIR / TEST_FILES["amber_inpcrd"])
    topology_file_path = str(TEST_DATA_DIR / TEST_FILES["amber_topology"])

    result_all_res = single_frame_contact_analysis(
        coordinates_file=coord_file_path,
        topology_file=topology_file_path,
        out_file="tmp.tmp",
    )

    result_p1 = single_frame_contact_analysis(
        coordinates_file=coord_file_path,
        topology_file=topology_file_path,
        out_file="tmp.tmp",
        first_res=1,
        last_res=100,
    )

    result_p2 = single_frame_contact_analysis(
        coordinates_file=coord_file_path,
        topology_file=topology_file_path,
        out_file="tmp.tmp",
        first_res=101,
    )

    assert len(result_all_res) == len(result_p1) + len(result_p2)


def test_traject():
    """
    Test a 5 frame trajectory gives expected result
    """
    trajectory_file_path = str(TEST_DATA_DIR / TEST_FILES["pdb_traject"])

    result = multi_frame_contact_analysis(
        trajectory_file=trajectory_file_path,
        out_file="tmp.tmp",
        first_res=1,
        last_res=20,
    )
    assert result.shape == (5, 157)


def test_multi_frame_pdb():
    """
    Test a 5 frame pdb gives expected result.
    """
    trajectory_file_path = str(TEST_DATA_DIR / TEST_FILES["pdb_traject"])

    result = multi_frame_contact_analysis(
        trajectory_file=trajectory_file_path,
        out_file="tmp.tmp",
        first_res=1,
        last_res=20,
    )

    assert result.shape == (5, 157)
