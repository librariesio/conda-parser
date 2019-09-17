from conda.api import Solver
from urllib.parse import unquote


def package_info(channel: str, name: str, version: str) -> dict:
    channel, name, version = unquote_params(channel, name, version)

    # join the name and version together with equals if it's provided
    spec = "==".join([name, version]) if version else name

    # solve the spec for this package.
    packages = Solver(".", [channel], specs_to_add=[spec]).solve_final_state()

    # find the package passed in, it will be there, as Solver rasies if not found
    first_package_record = [dep for dep in packages if dep.name == name][0]
    return dict(first_package_record.dump())


def unquote_params(*args: str) -> list:
    return [unquote(arg) for arg in args]
