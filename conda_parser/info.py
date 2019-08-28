from conda.api import Solver
from conda.exceptions import ResolvePackageNotFound


def package_info(channel: str, package: str, version: str) -> dict:
    # join the package and version together
    spec = f"{package}{version}"

    try:
        # solve the spec for this package.
        packages = Solver(".", [channel], specs_to_add=[spec]).solve_final_state()
    except ResolvePackageNotFound:
        return {"error": f"Errror: {spec} not found"}

    # find the package passed in
    record = dict([dep for dep in packages if dep.name == package][0].dump())

    # Clear out some unneeded keys
    del record["arch"]
    del record["build_number"]
    del record["constrains"]
    del record["fn"]
    del record["subdir"]

    return record
