import typing

import yaml
import re
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


def read_environment(environment_file: str) -> dict:
    """
        Loads the file into yaml and returns the keys that we care about.
            example: ignores `prefix:` settings in environment.yml
    """
    environment = yaml.load(environment_file, Loader=Loader)
    return {k: v for k, v in environment.items() if k in FILTER_KEYS}


def parse_environment(filename: str, environment_file: str) -> dict:
    """
        Loads a file, checks some common error conditions, tries its best
        to see if it is an actual Conda environment.yml file, and if it is,
        it will return a dictionary of a list of the manifest, lockfile, and channels.

        returns
            - dict of "error": "message"
            or
            - dict of "lockfile", "manifest", "channels"
    """
    # we need the `file` field
    if not environment_file:
        return {"error": "No `file` provided."}

    # file must be in .yaml or .yml format
    if not filename or not allowed_filename(filename):
        return {"error": "Please provide a `.yml` or `.yaml` environment file"}

    # Parse the file
    try:
        environment = read_environment(environment_file)
    except yaml.YAMLError as exc:
        return {"error": f"YAML parsing error in environment file: {exc}"}

    if not environment.get("dependencies"):
        return {"error": f"No `dependencies:` in your {filename}"}

    # Ignore pip for now.
    environment["dependencies"] = clean_out_pip(environment["dependencies"])

    lockfile = solve_environment(environment)
    manifest = resolve_manifest_versions(environment["dependencies"], lockfile)

    return {
        "manifest": sorted(manifest, key=lambda i: i["name"]),
        "lockfile": sorted(lockfile, key=lambda i: i["name"]),
        "channels": sorted(environment["channels"]),
    }


def clean_out_pip(specs: list) -> list:
    """ Not supporting pip for now """
    return [spec for spec in specs if isinstance(spec, str)]


def solve_environment(environment: dict) -> dict:
    """
        Using the Conda API, Solve an environment, get back all
        of the dependencies.

        returns a list of {"name": name, "requirement": requirement} values.
    """
    prefix = environment.get("prefix", ".")
    channels = environment["channels"]
    specs = environment["dependencies"]

    dependencies = Solver(prefix, channels, specs_to_add=specs).solve_final_state()

    return [
        {"name": dep["name"], "requirement": dep["version"]} for dep in dependencies
    ]


def resolve_manifest_versions(specs: list, dependencies: list) -> list:
    """
        This resolves a manifest from what the environment.yml passed in
        by finding the versions that were Solved

        returns a list of {"name": name, "requirement": requirement} values.
    """
    reg = re.compile(r"[\w\-\.]+")
    spec_names = [reg.match(spec).group(0) for spec in specs]

    return [req for req in dependencies if req["name"] in spec_names]
