import typing

import yaml
from yaml import CDumper as Dumper
from yaml import CLoader as Loader

ALLOWED_EXTENSIONS = {"yml", "yaml"}  # Only file extensions that are allowed
FILTER_KEYS = {
    "dependencies",
    "channels",
}  # What keys we want back from the environment file


def allowed_filename(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def read_environment(file: typing.BinaryIO) -> dict:
    """
        Loads the file into yaml and returns the keys that we care about.
            example: ignores `prefix:` settings in environment.yml
    """
    environment = yaml.load(file.read(), Loader=Loader)
    return {k: v for k, v in environment.items() if k in FILTER_KEYS}


def parse_file(file: typing.BinaryIO) -> dict:
    """
        Loads a file, checks some common error conditions, tries its best
        to see if it is an actual Conda environment.yml file, and if it is,
        it will return a dictionary of a list of the dependencies and channels.

        returns
            - dict of "error": "message"
            or
            - dict of "dependencies", "channels"
    """
    # we need the `file` field
    if not file:
        return {"error": "No `file` provided."}

    # file must be in .yaml or .yml format
    # Support BinaryIO and BufferedReader
    filename = file.filename if hasattr(file, "filename") else file.name
    if not allowed_filename(filename):
        return {"error": "Please provide a `.yml` or `.yaml` environment file"}

    # Parse the file
    try:
        environment = read_environment(file)
    except yaml.YAMLError as exc:
        return {"error": f"YAML parsing error in environment file: {exc}"}

    dependencies = environment.get("dependencies")
    if not dependencies:
        return {"error": f"No `dependencies:` in your {filename}"}

    return {
        "dependencies": parse_dependencies(dependencies),
        "channels": environment.get("channels", []),
    }


def parse_dependencies(raw_dependencies: list) -> dict:
    """
        Loop through the dependencies list, get the name/requirement
        Filter out anything that is not a string (such as pip: key)

        Parameters:
            raw_dependencies: a list of dependency strings

        returns:
            list of dict of name/requirement values

    """
    dependencies = []

    for dep in raw_dependencies:
        if isinstance(dep, str):
            dependencies.append(parse_dependency(dep))

    return dependencies


def parse_dependency(dependency: str) -> dict:
    """
        Get the name and requirement from a dependency string

        Matches:
         https://docs.conda.io/projects/conda-build/en/latest/resources/package-spec.html#package-match-specifications

        returns:
            dict of name/requirement values
    """
    if " " in dependency:
        parts = dependency.split(" ")
        name = parts[0]
        requirement = parts[1].lstrip("==")
    else:
        parts = dependency.split("=")
        parts.append(
            ">= 0"
        )  # Default Requirement. Appending because no requirement specified, will get sliced into return.
        name, requirement = parts[:2]

    return {"name": name, "requirement": requirement}
