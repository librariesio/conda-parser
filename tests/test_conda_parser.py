from conda_parser.parse import (
    FILTER_KEYS,
    allowed_filename,
    parse_environment,
    clean_out_pip,
    read_environment,
    solve_environment,
    match_specs,
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
        environment = read_environment(all_styles.read())

    for key in environment.keys():
        assert key in FILTER_KEYS
    assert "name" not in environment


def test_parse_environment_errors_no_file():
    """
    Checking a few of the standard errors
    - No file provided
    """
    parsed = parse_environment(None, None)
    assert parsed["error"] == "No `file` provided."


def test_parse_environment_errors_wrong_filetype():
    """
    Checking a few of the standard errors
    - Disallowed filename
    """
    with open("tests/fixtures/not_a_yaml.md", "rb") as f:
        parsed = parse_environment("not_a_yaml.md", f)
    assert parsed["error"] == "Please provide a `.yml` or `.yaml` environment file"


def test_parse_environment_errors_yaml_error():
    """
    Checking a few of the standard errors
    - YAML errors
    """
    with open("tests/fixtures/bad_yaml.yml", "rb") as bad_yaml:
        parsed = parse_environment("bad_yaml.yml", bad_yaml)
    assert parsed["error"].startswith(
        "YAML parsing error in environment file: while parsing a block collection"
    )


def test_parse_environment_errors_no_dependencies():
    """
    Checking a few of the standard errors
    - No dependencies in environment.yml
    """
    with open("tests/fixtures/no_dependencies.yml", "rb") as no_dependencies:
        parsed = parse_environment("no_dependencies.yml", no_dependencies)
    assert parsed["error"] == "No `dependencies:` in your no_dependencies.yml"


def test_solve_environment(mocker, fake_sqlite_deps):
    """ testing parsing POST """
    mocker.patch("conda.api.Solver.solve_final_state", side_effect=fake_sqlite_deps)
    sqlite_dependencies, _ = solve_environment(
        {"channels": ["conda-forge"], "dependencies": [{"name": "sqlite"}]}
    )
    assert {"name": "ncurses", "requirement": "6.1"} in sqlite_dependencies


def test_clean_out_pip():
    """ testing removing pip from specs """
    specs = ["zlib=1.2.11=0", {"pip": ["werkzeug==0.12.2"]}]
    assert clean_out_pip(specs) == ["zlib=1.2.11=0"]


def test_match_specs():
    inputs = {
        "numpy": {"name": "numpy", "requirement": ""},
        "numpy 1.8.*": {"name": "numpy", "requirement": "1.8.*"},
        "numpy 1.8*": {"name": "numpy", "requirement": "1.8.*"},
        "numpy 1.8.1": {"name": "numpy", "requirement": "1.8.1"},
        "numpy >=1.8": {"name": "numpy", "requirement": ">=1.8"},
        "numpy ==1.8.1": {"name": "numpy", "requirement": "1.8.1"},
        "numpy 1.8|1.8*": {"name": "numpy", "requirement": "1.8|1.8.*"},
        "numpy >=1.8,<2": {"name": "numpy", "requirement": ">=1.8,<2"},
        "numpy >=1.8,<2|1.9": {"name": "numpy", "requirement": ">=1.8,<2|1.9"},
        "numpy 1.8.1 py27_0": {"name": "numpy", "requirement": "1.8.1"},
        "numpy=1.8.1=py27_0": {"name": "numpy", "requirement": "1.8.1"},
    }

    for testing, expected in inputs.items():
        assert (match_specs([testing])) == [expected]
