from conda.api import Solver


def package_info(channel: str, package: str, version: str) -> dict:
    spec = f"{package}{version}"
    packages = Solver(".", [channel], specs_to_add=[spec]).solve_final_state()
    record = [dep for dep in packages if dep.name == package][0]
    return dict(record.dump())
