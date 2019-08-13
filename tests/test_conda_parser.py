import pytest

from conda_parser.parse import (
    FILTER_KEYS,
    allowed_filename,
    parse_dependency,
    parse_file,
    read_environment,
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
    for key in FILTER_KEYS:
        assert key in environment
    assert "name" not in environment


def test_parse_file_errors_no_file():
    """
    Checking a few of the standard errors
    - No file provided
    """
    parsed = parse_file(None)
    assert parsed["error"] == "No `file` provided."


def test_parse_file_errors_wrong_filetype():
    """
    Checking a few of the standard errors
    - Disallowed filename
    """
    with open("README.md", "rb") as f:
        parsed = parse_file(f)
    assert parsed["error"] == "Please provide a `.yml` or `.yaml` environment file"


def test_parse_file_errors_yaml_error():
    """
    Checking a few of the standard errors
    - YAML errors
    """
    with open("tests/fixtures/bad_yaml.yml", "rb") as bad_yaml:
        parsed = parse_file(bad_yaml)
    assert parsed["error"].startswith(
        "YAML parsing error in environment file: while parsing a block collection"
    )


def test_parse_file_errors_no_dependencies():
    """
    Checking a few of the standard errors
    - No dependencies in environment.yml
    """
    with open("tests/fixtures/no_dependencies.yml", "rb") as no_dependencies:
        parsed = parse_file(no_dependencies)
    assert (
        parsed["error"]
        == "No `dependencies:` in your tests/fixtures/no_dependencies.yml"
    )


def test_parse_dependency():
    """ Test all the different valid values. """

    def _test_parse_dependency(line, requirement):
        """ Helper method to keep this test clean """
        dep = parse_dependency(line)
        assert dep["name"] == "numpy"
        assert dep["requirement"] == requirement

    _test_parse_dependency("numpy", ">= 0")
    _test_parse_dependency("numpy 1.8*", "1.8*")
    _test_parse_dependency("numpy 1.8.1", "1.8.1")
    _test_parse_dependency("numpy >=1.8", ">=1.8")
    _test_parse_dependency("numpy ==1.8.1", "1.8.1")
    _test_parse_dependency("numpy 1.8|1.8*", "1.8|1.8*")
    _test_parse_dependency("numpy >=1.8,<2", ">=1.8,<2")
    _test_parse_dependency("numpy >=1.8,<2|1.9", ">=1.8,<2|1.9")
    _test_parse_dependency("numpy 1.8.1 py27_0", "1.8.1")
    _test_parse_dependency("numpy=1.8.1=py27_0", "1.8.1")


def test_parse_file():
    with open("tests/fixtures/all_styles.yml", "rb") as all_styles:
        parsed = parse_file(all_styles)

    dependencies = [
        {"name": "numpy", "requirement": ">= 0"},
        {"name": "numpy", "requirement": "1.8*"},
        {"name": "numpy", "requirement": "1.8.1"},
        {"name": "numpy", "requirement": ">=1.8"},
        {"name": "numpy", "requirement": "1.8.1"},
        {"name": "numpy", "requirement": "1.8|1.8*"},
        {"name": "numpy", "requirement": ">=1.8,<2"},
        {"name": "numpy", "requirement": ">=1.8,<2|1.9"},
        {"name": "numpy", "requirement": "1.8.1"},
        {"name": "numpy", "requirement": "1.8.1"},
    ]
    assert parsed["dependencies"] == dependencies
    assert parsed["channels"] == ["anaconda"]


def test_parse_file_no_pip():
    with open("tests/fixtures/with_pip.yml", "rb") as with_pip:
        parsed = parse_file(with_pip)
    assert len(parsed["dependencies"]) == 0
