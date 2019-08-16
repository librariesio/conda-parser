# conftest.py - This is used to configure pytest to have a fixture for the Flask App
import pytest

from conda_parser import create_app


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
