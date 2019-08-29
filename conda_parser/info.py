from conda.api import Solver


def package_info(channel: str, package: str, version: str) -> dict:
    # join the package and version together
    spec = f"{package}{version}"

    # solve the spec for this package.
    packages = Solver(".", [channel], specs_to_add=[spec]).solve_final_state()

    # find the package passed in, it will be there, as Solver rasies if not found
    first_package_record = [dep for dep in packages if dep.name == package][0]
    record = dict(first_package_record.dump())

    # Only keep needed keys.
    KEYS = [
        "build",
        "channel",
        "depends",
        "license",
        "license_family",
        "md5",
        "name",
        "platform",
        "sha256",
        "size",
        "timestamp",
        "url",
        "version",
    ]
    return {k: record[k] for k in KEYS}
