# conftest.py - This is used to configure pytest to have a fixture for the Flask App
import pytest

from conda_parser import create_app
from conda.models.records import PackageRecord


@pytest.fixture
def app():
    app = create_app()
    app.debug = True
    return app


@pytest.fixture
def fake_numpy_deps():
    """ Returns a lambda that returns this faked data so we can mock side_effect it"""
    deps = [
        ("blas", "1.0"),
        ("ca-certificates", "2019.5.15"),
        ("intel-openmp", "2019.4"),
        ("libcxxabi", "4.0.1"),
        ("libgfortran", "3.0.1"),
        ("xz", "5.2.4"),
        ("zlib", "1.2.11"),
        ("libcxx", "4.0.1"),
        ("mkl", "2019.4"),
        ("openssl", "1.1.1"),
        ("tk", "8.6.8"),
        ("libffi", "3.2.1"),
        ("ncurses", "6.1"),
        ("libedit", "3.1.20181209"),
        ("readline", "7.0"),
        ("sqlite", "3.29.0"),
        ("python", "3.7.4"),
        ("certifi", "2019.6.16"),
        ("numpy-base", "1.16.4"),
        ("mkl_random", "1.0.2"),
        ("setuptools", "41.0.1"),
        ("wheel", "0.33.4"),
        ("pip", "19.1.1"),
        ("mkl_fft", "1.0.12"),
        ("numpy", "1.16.4"),
    ]
    return lambda: [dict(name=v[0], version=v[1]) for v in deps]


@pytest.fixture
def fake_sqlite_deps():
    return lambda: [
        {"name": "libcxxabi", "version": "8.0.0"},
        {"name": "libcxx", "version": "8.0.0"},
        {"name": "ncurses", "version": "6.1"},
        {"name": "readline", "version": "8.0"},
        {"name": "sqlite", "version": "3.29.0"},
    ]


@pytest.fixture
def package_and_version_strings():
    return [
        "_ipyw_jlab_nb_ext_conf=0.1.0=py37_0",
        "alabaster=0.7.12=py37_0",
        "anaconda-navigator=1.9.7=py37_0",
        "asn1crypto=0.24.0=py37_0",
        "astroid >=2.2.5",
        "backports.functools_lru_cache=1.5=py_2",
        "bzip2=1.0.8=h7b6447c_0",
        "ca-certificates=2019.5.15=0",
        "conda===4.7.11=py37",
        "conda-build",
        "conda-env 2.6.0",
    ]


@pytest.fixture
def package_and_version_dicts():
    return [
        {"name": "_ipyw_jlab_nb_ext_conf", "version": "0.1.0"},
        {"name": "alabaster", "version": "0.7.12"},
        {"name": "anaconda-navigator", "version": "1.9.7"},
        {"name": "asn1crypto", "version": "0.24.0"},
        {"name": "astroid", "version": "2.2.5"},
        {"name": "backports.functools_lru_cache", "version": "1.5"},
        {"name": "blas", "version": "1.0"},
        {"name": "bleach", "version": "3.1.0"},
        {"name": "blosc", "version": "1.16.3"},
        {"name": "bokeh", "version": "1.2.0"},
        {"name": "boto", "version": "2.49.0"},
        {"name": "bottleneck", "version": "1.2.1"},
        {"name": "bzip2", "version": "1.0.8"},
        {"name": "ca-certificates", "version": "2019.5.15"},
        {"name": "cairo", "version": "1.14.12"},
        {"name": "certifi", "version": "2019.6.16"},
        {"name": "cffi", "version": "1.12.3"},
        {"name": "chardet", "version": "3.0.4"},
        {"name": "click", "version": "7.0"},
        {"name": "cloudpickle", "version": "1.2.1"},
        {"name": "clyent", "version": "1.2.2"},
        {"name": "colorama", "version": "0.4.1"},
        {"name": "conda", "version": "4.7.11"},
        {"name": "conda-build", "version": "3.18.8"},
        {"name": "conda-env", "version": "2.6.0"},
    ]


@pytest.fixture
def solved_urllib3():
    fake = [
        PackageRecord(
            **{
                "arch": None,
                "build": "py36_0",
                "build_number": 0,
                "channel": "https://conda.anaconda.org/conda-forge/linux-64",
                "constrains": [],
                "depends": [
                    "certifi",
                    "cryptography >=1.3.4",
                    "idna >=2.0.0",
                    "pyopenssl >=0.14",
                    "pysocks >=1.5.6,<2.0,!=1.5.7",
                    "python >=3.6,<3.7.0a0",
                ],
                "fn": "urllib3-1.25.3-py36_0.tar.bz2",
                "license": "MIT",
                "license_family": "MIT",
                "md5": "98696f9f012d04bd7795a6a2febf66a0",
                "name": "urllib3",
                "platform": None,
                "sha256": "d94eb3db911a6806f45a9fba50e49961c189d9fb32c44f8fd19902334616335e",
                "size": 191254,
                "subdir": "linux-64",
                "timestamp": 1558705030958,
                "url": "https://conda.anaconda.org/conda-forge/linux-64/urllib3-1.25.3-py36_0.tar.bz2",
                "version": "1.25.3",
            }
        ),
        PackageRecord(
            **{
                "arch": None,
                "build": "py36_0",
                "build_number": 0,
                "channel": "https://conda.anaconda.org/conda-forge/linux-64",
                "constrains": [],
                "depends": [
                    "certifi",
                    "cryptography >=1.3.4",
                    "idna >=2.0.0",
                    "pyopenssl >=0.14",
                    "pysocks >=1.5.6,<2.0,!=1.5.7",
                    "python >=3.6,<3.7.0a0",
                ],
                "fn": "urllib3-1.25.3-py36_0.tar.bz2",
                "license": "MIT",
                "license_family": "MIT",
                "md5": "98696f9f012d04bd7795a6a2febf66a0",
                "name": "not-urllib3",
                "platform": None,
                "sha256": "d94eb3db911a6806f45a9fba50e49961c189d9fb32c44f8fd19902334616335e",
                "size": 191254,
                "subdir": "linux-64",
                "timestamp": 1558705030958,
                "url": "https://conda.anaconda.org/conda-forge/linux-64/urllib3-1.25.3-py36_0.tar.bz2",
                "version": "1.25.3",
            }
        ),
    ]
    return lambda: fake


@pytest.fixture
def expected_result_urllib3():
    return {
        "arch": None,
        "build": "py36_0",
        "build_number": 0,
        "channel": "https://conda.anaconda.org/conda-forge/linux-64",
        "constrains": [],
        "depends": [
            "certifi",
            "cryptography >=1.3.4",
            "idna >=2.0.0",
            "pyopenssl >=0.14",
            "pysocks >=1.5.6,<2.0,!=1.5.7",
            "python >=3.6,<3.7.0a0",
        ],
        "fn": "urllib3-1.25.3-py36_0.tar.bz2",
        "license": "MIT",
        "license_family": "MIT",
        "md5": "98696f9f012d04bd7795a6a2febf66a0",
        "name": "urllib3",
        "platform": None,
        "sha256": "d94eb3db911a6806f45a9fba50e49961c189d9fb32c44f8fd19902334616335e",
        "size": 191254,
        "subdir": "linux-64",
        "timestamp": 1558705030958,
        "url": "https://conda.anaconda.org/conda-forge/linux-64/urllib3-1.25.3-py36_0.tar.bz2",
        "version": "1.25.3",
    }

@pytest.fixture
def record_not_found():
    from conda.exceptions import ResolvePackageNotFound

    return (ResolvePackageNotFound(bad_deps=[["whoami", "==1.25.3"]]),)
