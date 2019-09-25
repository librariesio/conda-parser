from conda_parser.parse import (
    FILTER_KEYS,
    allowed_filename,
    parse_environment,
    clean_out_pip,
    read_environment,
    solve_environment,
    resolve_manifest_versions,
    pin_spec_to_name_version,
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
    sqlite_dependencies = solve_environment(
        {"channels": ["conda-forge"], "dependencies": ["sqlite"]}
    )[0]
    assert {"name": "ncurses", "requirement": "6.1"} in sqlite_dependencies


def test_clean_out_pip():
    """ testing removing pip from specs """
    specs = ["zlib=1.2.11=0", {"pip": ["werkzeug==0.12.2"]}]
    assert clean_out_pip(specs) == ["zlib=1.2.11=0"]


def test_resolve_manifest_versions(
    package_and_version_strings, package_and_version_dicts
):
    resolved = resolve_manifest_versions(
        package_and_version_strings, package_and_version_dicts
    )

    # Assert at least some change was made
    assert package_and_version_strings != resolved

    assert resolved == [
        {"name": "_ipyw_jlab_nb_ext_conf", "version": "0.1.0"},
        {"name": "alabaster", "version": "0.7.12"},
        {"name": "anaconda-navigator", "version": "1.9.7"},
        {"name": "asn1crypto", "version": "0.24.0"},
        {"name": "astroid", "version": "2.2.5"},
        {"name": "backports.functools_lru_cache", "version": "1.5"},
        {"name": "bzip2", "version": "1.0.8"},
        {"name": "ca-certificates", "version": "2019.5.15"},
        {"name": "conda", "version": "4.7.11"},
        {"name": "conda-build", "version": "3.18.8"},
        {"name": "conda-env", "version": "2.6.0"},
    ]


def test_pin_spec_to_name_version():
    inputs = {
        "numpy": "numpy",
        "numpy 1.8*": "numpy 1.8.*",
        "numpy 1.8.1": "numpy 1.8.1",
        "numpy >=1.8": "numpy >=1.8",
        "numpy ==1.8.1": "numpy 1.8.1",
        "numpy 1.8|1.8*": "numpy 1.8|1.8.*",
        "numpy >=1.8,<2": "numpy >=1.8,<2",
        "numpy >=1.8,<2|1.9": "numpy >=1.8,<2|1.9",
        "numpy 1.8.1 py27_0": "numpy 1.8.1",
        "numpy=1.8.1=py27_0": "numpy 1.8.1",
    }

    for testing, expected in inputs.items():
        assert (pin_spec_to_name_version([testing])) == [expected]
