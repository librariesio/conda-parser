import typing

import yaml
from conda.api import Solver
from yaml import CDumper as Dumper
from yaml import CLoader as Loader

ALLOWED_EXTENSIONS = {"yml", "yaml"}  # Only file extensions that are allowed
FILTER_KEYS = {
    "dependencies",
    "channels",
    "prefix",
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


def parse_environment(file: typing.BinaryIO) -> dict:
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

    if not environment.get("dependencies"):
        return {"error": f"No `dependencies:` in your {filename}"}

    return {
        "dependencies": solve_environment(environment),
        "channels": environment.get("channels", []),
    }


def solve_environment(environment: dict) -> dict:
    prefix = environment.get("prefix", ".")
    channels = environment["channels"]
    specs = environment["dependencies"]

    dependencies = Solver(prefix, channels, specs_to_add=specs).solve_final_state()

    return [
        {"name": dep["name"], "requirement": dep["version"]} for dep in dependencies
    ]
