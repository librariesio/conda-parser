import pytest

from conda_parser.parse import (
    FILTER_KEYS,
    allowed_filename,
    parse_environment,
    read_environment,
    solve_environment,
)


def test_allowed_filename_good():
    """ Testing that yml and yaml are good filetypes """
    good_names = ["hello.yml", "hello.yaml"]
    for good_name in good_names:
        assert allowed_filename(good_name) == True


def test_allowed_filename_bad():
    """ Testing that only yml and yaml files are allowed """
    bad_names = ["requirements.txt", "helloworld", ".bashrc"]
    for bad_name in bad_names:
        assert allowed_filename(bad_name) == False


def test_read_environment_filter_keys():
    """ Testing that read environment works and filters properly """
    with open("tests/fixtures/all_styles.yml", "rb") as all_styles:
        environment = read_environment(all_styles)

    for key in environment.keys():
        assert key in FILTER_KEYS
    assert "name" not in environment


def test_parse_environment_errors_no_file():
    """
    Checking a few of the standard errors
    - No file provided
    """
    parsed = parse_environment(None)
    assert parsed["error"] == "No `file` provided."


def test_parse_environment_errors_wrong_filetype():
    """
    Checking a few of the standard errors
    - Disallowed filename
    """
    with open("tests/fixtures/not_a_yaml.md", "rb") as f:
        parsed = parse_environment(f)
    assert parsed["error"] == "Please provide a `.yml` or `.yaml` environment file"


def test_parse_environment_errors_yaml_error():
    """
    Checking a few of the standard errors
    - YAML errors
    """
    with open("tests/fixtures/bad_yaml.yml", "rb") as bad_yaml:
        parsed = parse_environment(bad_yaml)
    assert parsed["error"].startswith(
        "YAML parsing error in environment file: while parsing a block collection"
    )


def test_parse_environment_errors_no_dependencies():
    """
    Checking a few of the standard errors
    - No dependencies in environment.yml
    """
    with open("tests/fixtures/no_dependencies.yml", "rb") as no_dependencies:
        parsed = parse_environment(no_dependencies)
    assert (
        parsed["error"]
        == "No `dependencies:` in your tests/fixtures/no_dependencies.yml"
    )


def test_solve_environment(mocker, fake_sqlite_deps):
    """ testing parsing POST """
    mocker.patch("conda.api.Solver.solve_final_state", side_effect=fake_sqlite_deps)
    sqlite_dependencies = solve_environment(
        {"channels": ["conda-forge"], "dependencies": ["sqlite"]}
    )
    assert {"name": "ncurses", "requirement": "6.1"} in sqlite_dependencies
