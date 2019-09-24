import typing

import yaml
import re
from conda.api import Solver
from conda.exceptions import ResolvePackageNotFound
from yaml import CDumper as Dumper
from yaml import CLoader as Loader
from pprint import pprint

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

    lockfile, bad_packages = solve_environment(environment)
    manifest = resolve_manifest_versions(environment["dependencies"], lockfile)

    output = {
        "manifest": sorted(manifest, key=lambda i: i["name"]),
        "lockfile": sorted(lockfile, key=lambda i: i["name"]),
        "channels": sorted(environment["channels"]),
    }
    if bad_packages:
        output["bad_packages"] = sorted(bad_packages)

    return output


def clean_out_pip(specs: list) -> list:
    """ Not supporting pip for now """
    return [spec for spec in specs if isinstance(spec, str)]


def clean_out_urls(channels: list) -> list:
    """
    Grab channels from the environment file, but remove any that are urls.
    From experience parsing these channels, they are mostly artifactory urls, which
    are behind vpns, so we can't access them anyway
    """
    return [channel for channel in channels if "://" not in channel]


def try_to_fix_specs(specs: list) -> list:
    _specs = []
    for dep in specs:
        parts = [
            d for d in dep.split("=") if d
        ]  # Remove empty string coming between `==`
        _specs.append("==".join(parts[:2]))
    return _specs


def solve_environment(environment: dict) -> dict:
    """
        Using the Conda API, Solve an environment, get back all
        of the dependencies.

        returns a list of {"name": name, "requirement": requirement} values.
    """
    prefix = environment.get("prefix", ".")
    channels = clean_out_urls(environment["channels"])
    # pprint(environment)
    specs = try_to_fix_specs(environment["dependencies"])

    bad_specs = None
    try:
        dependencies = Solver(prefix, channels, specs_to_add=specs).solve_final_state()
    except ResolvePackageNotFound as e:
        good_specs, bad_specs = rigidly_parse_error_message(e.message, specs)
        dependencies = Solver(
            prefix, channels, specs_to_add=good_specs
        ).solve_final_state()

    return (
        [{"name": dep["name"], "requirement": dep["version"]} for dep in dependencies],
        bad_specs,
    )


def resolve_manifest_versions(specs: list, dependencies: list) -> list:
    """
        This resolves a manifest from what the environment.yml passed in
        by finding the versions that were Solved

        returns a list of {"name": name, "requirement": requirement} values.
    """
    reg = re.compile(r"[\w\-\.]+")
    spec_names = [reg.match(spec).group(0) for spec in specs]

    return [req for req in dependencies if req["name"] in spec_names]


def rigidly_parse_error_message(message: str, specs: list) -> typing.Tuple[list, list]:
    message = message.split("\n")  # split by newlines
    message.pop(0)  # remove the error message header
    chains = [chain.lstrip("  - ") for chain in message]

    good = set(specs) - set(chains)
    bad = set(chains)

    return list(good), list(bad)
