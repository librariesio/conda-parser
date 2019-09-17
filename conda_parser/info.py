from conda.api import Solver
from urllib.parse import unquote


def package_info(channel: str, package: str, version: str) -> dict:
    channel, package, version = unquote_params(channel, package, version)

    # join the package and version together
    spec = f"{package}{version}"

    # solve the spec for this package.
    packages = Solver(".", [channel], specs_to_add=[spec]).solve_final_state()

    # find the package passed in, it will be there, as Solver rasies if not found
    first_package_record = [dep for dep in packages if dep.name == package][0]
    return dict(first_package_record.dump())


def unquote_params(*args: str) -> list:
    return [unquote(arg) for arg in args]
