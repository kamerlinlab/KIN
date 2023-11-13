"""
Tests for pymol_projections module. 
"""
from pathlib import Path
import pytest
from kin.pymol_projections import (
    project_pymol_res_res_scores,
    project_pymol_per_res_scores,
    gen_per_res_scores,
    _save_pymol_file,
    _rescale_scores,
)


#### fixtures
@pytest.fixture
def example_res_res_scores() -> dict[tuple[int, int], float]:
    return {(1, 2): 0.5, (3, 4): 0.8, (5, 6): 0.2}


@pytest.fixture
def example_res_res_colors() -> dict[tuple[int, int], str]:
    return {(1, 2): "blue", (3, 4): "green", (5, 6): "yellow"}


@pytest.fixture
def example_per_res_scores() -> dict[int, float]:
    return {1: 0.5, 2: 0.1, 3: 1.0, 4: 0}


#### tests for project_pymol_res_res_scores
def test_project_pymol_res_res_scores(
    tmpdir: Path,
    example_res_res_scores: dict[tuple[int, int], float],
    example_res_res_colors: dict[tuple[int, int], str],
):
    """Test outputted file"""
    out_file = str(tmpdir.join("test_script.pml"))

    project_pymol_res_res_scores(
        example_res_res_scores, out_file, example_res_res_colors
    )

    # Verify the contents of the generated PyMOL script
    with open(out_file, "r", encoding="utf-8") as file_in:
        contents = file_in.read()
        for radii in [0.1875, 0.3, 0.075]:
            assert str(radii) in contents
        for color in ["green", "blue", "yellow"]:
            assert color in contents
        for resnumbs in [(1, 2), (3, 4), (5, 6)]:
            res1, res2 = resnumbs
            resid_str = f"resid {str(res1)} and name CA, resid {str(res2)} and name CA"
            assert resid_str in contents


def test_project_pymol_res_res_scores_no_colors(
    tmpdir: Path, example_res_res_scores: dict[tuple[int, int], float]
):
    """test with no colours used, so no color but red should be added."""
    out_file = str(tmpdir.join("test_script_no_colors.pml"))

    project_pymol_res_res_scores(example_res_res_scores, out_file)

    # Verify the contents of the generated PyMOL script
    with open(out_file, "r", encoding="utf-8") as file_in:
        contents = file_in.read()
        assert "# To use this script" in contents
        for radii in [0.1875, 0.3, 0.075]:
            assert str(radii) in contents
        for color in ["green", "blue", "yellow"]:
            assert color not in contents
        for resnumbs in [(1, 2), (3, 4), (5, 6)]:
            res1, res2 = resnumbs
            resid_str = f"resid {str(res1)} and name CA, resid {str(res2)} and name CA"
            assert resid_str in contents


#### tests for project_pymol_per_res_scores
def test_project_pymol_per_res_scores(
    tmpdir: Path, example_per_res_scores: dict[int, float]
):
    """Test outputted file"""
    out_file = str(tmpdir.join("test_script.pml"))

    project_pymol_per_res_scores(
        per_res_scores=example_per_res_scores,
        out_file=out_file,
    )

    # Verify the contents of the generated PyMOL script
    with open(out_file, "r", encoding="utf-8") as file_in:
        contents = file_in.read()
        scales = ["0.5000", "0.1000", "1.0000", "0.0000"]
        for res_numb, scale in enumerate(scales, start=1):
            res_line = rf"set sphere_scale, {scale}, resi {str(res_numb)} and name CA"
            assert res_line in contents


#### tests for gen_per_res_scores
def test_gen_per_res_scores_empty_input():
    """Test, empty input fails"""
    with pytest.raises(ZeroDivisionError):
        _ = gen_per_res_scores({})


def test_gen_per_res_scores_single_residue():
    """Test with a single residue"""
    result = gen_per_res_scores({(1, 1): 0.5})
    assert result == {1: 1.0}


def test_gen_per_res_scores_multiple_residues(
    example_res_res_scores: dict[tuple[int, int], float]
):
    """Test multiple residues"""
    res_res_scores = example_res_res_scores
    result = gen_per_res_scores(res_res_scores)
    assert result == {1: 0.625, 2: 0.625, 3: 1.0, 4: 1.0, 5: 0.25, 6: 0.25}


def test_gen_per_res_scores_max_val_is_1(
    example_res_res_scores: dict[tuple[int, int], float]
):
    """Test output max is 1.0"""
    result = gen_per_res_scores(example_res_res_scores)
    max_value = max(result.values())
    assert max_value == 1.0


#### tests for _save_pymol_file
def test_save_pymol_file(tmpdir):
    """Simple test to see if file contents written."""
    out_file = str(tmpdir.join("test_output.pml"))
    contents = "Test contents."
    _save_pymol_file(out_file, contents)
    assert Path(out_file).exists()

    # Check the content of the file
    with open(out_file, "r", encoding="utf-8") as file_in:
        assert file_in.read() == contents


#### tests for _rescale_scores
test_data = [
    (
        {"A": 10.0, "B": 20.0, "C": 30.0},
        100.0,
        {"A": 33.3333, "B": 66.6667, "C": 100.0},
    ),
    (
        {"X": 5.0, "Y": 10.0, "Z": 15.0},
        50.0,
        {"X": 16.6667, "Y": 33.3333, "Z": 50.0},
    ),
    ({"X": 25.0}, 50.0, {"X": 50.0}),
]


@pytest.mark.parametrize("input_dict, new_max_value, expected_result", test_data)
def test__rescale_scores(
    input_dict,
    new_max_value,
    expected_result,
):
    """Test standard scenarios"""
    assert _rescale_scores(input_dict, new_max_value) == expected_result


test_data = (
    ({"P": 0.0, "Q": 0.0, "R": 0.0}, 1.0, ZeroDivisionError),
    ({}, 1.0, ValueError),
)


@pytest.mark.parametrize("input_dict, new_max_value, error_type", test_data)
def test__rescale_scores_fails_on_null_values(input_dict, new_max_value, error_type):
    """Test standard scenarios"""
    with pytest.raises(error_type):
        _ = _rescale_scores(input_dict, new_max_value)


# Run the tests
if __name__ == "__main__":
    pytest.main()
