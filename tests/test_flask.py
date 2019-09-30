import io
import json

import pytest

from flask import url_for


def test_index(client):
    """ Sanity check """
    assert client.get(url_for("index")).status_code == 200


def _post_multipart(client, name, view="parse", force_solve=True):
    with open(name, "rb") as all_styles:
        data = {"file": (io.BytesIO(all_styles.read()), name)}
    return _post(client, data, view, "multipart/form-data", force_solve)


def _post_urlencoded(client, name, view="parse", force_solve=True):
    with open(name, "rb") as all_styles:
        data = {"file": all_styles.read(), "filename": name}
    return _post(client, data, view, "application/x-www-form-urlencoded", force_solve)


def _post(client, data, view, content_type, force_solve=True):
    if force_solve:
        url = url_for(view, force_solve=force_solve)
    else:
        url = url_for(view)

    return client.post(url, data=data, follow_redirects=True, content_type=content_type)


def test_parse_file(client, mocker, fake_numpy_deps):
    """ testing parsing POST """
    mocker.patch("conda.api.Solver.solve_final_state", side_effect=fake_numpy_deps)

    response = _post_urlencoded(client, "tests/fixtures/just_numpy.yml", "parse")
    assert response.status == "200 OK"

    response = _post_multipart(client, "tests/fixtures/just_numpy.yml", "parse")

    assert response.status == "200 OK"

    data = json.loads(response.data)

    assert data["channels"] == ["anaconda", "defaults"]
    assert {"name": "numpy-base", "requirement": "1.16.4"} in data["lockfile"]


def test_parse_file_no_force(client, mocker, fake_numpy_deps):
    response = _post_multipart(
        client, "tests/fixtures/just_numpy.yml", "parse", force_solve=False
    )

    assert response.status == "200 OK"
    data = json.loads(response.data)

    assert data["channels"] == ["anaconda", "defaults"]
    assert data["lockfile"] == []
    assert data["manifest"] == [{"name": "numpy", "requirement": "1.16.4"}]


def test_parse_file_no_force_lockfile(client, mocker, fake_numpy_deps):
    mocker.patch("conda.api.Solver.solve_final_state", side_effect=fake_numpy_deps)
    response = _post_multipart(
        client, "tests/fixtures/numpy.yml.lock", "parse", force_solve=False
    )

    assert response.status == "200 OK"
    data = json.loads(response.data)

    assert data["channels"] == ["anaconda", "defaults"]
    assert {"name": "numpy-base", "requirement": "1.16.4"} in data["lockfile"]


def test_parse_file_not_found(client, mocker, record_not_found):
    """ testing parsing POST """
    mocker.patch(
        "conda.api.Solver.solve_final_state", side_effect=[record_not_found, []]
    )

    response = _post_urlencoded(client, "tests/fixtures/just_numpy.yml", "parse")
    assert response.status == "200 OK"
    assert json.loads(response.data) == {
        "bad_specs": ["whoami -> ==1.25.3"],
        "channels": ["anaconda", "defaults"],
        "lockfile": [],
        "manifest": [{"name": "numpy", "requirement": "1.16.4"}],
    }


def test_package(client, mocker, solved_urllib3, expected_result_urllib3):
    mocker.patch("conda.api.Solver.solve_final_state", side_effect=solved_urllib3)

    # name and channel
    response = client.get(
        url_for("package", channel="anaconda", name="urllib3"), follow_redirects=True
    )
    assert response.status == "200 OK"
    data = json.loads(response.data)

    assert data["license"] == "MIT"

    # all parameters
    response = client.get(
        url_for("package", channel="anaconda", name="urllib3", version="1.25.3"),
        follow_redirects=True,
    )
    assert response.status == "200 OK"
    data = json.loads(response.data)

    assert data == expected_result_urllib3


def test_package_download(client, mocker, solved_urllib3, expected_result_urllib3):
    mocker.patch("conda.api.Solver.solve_final_state", side_effect=solved_urllib3)

    # name and channel
    response = client.get(
        url_for("package", channel="anaconda", name="urllib3", download=True)
    )
    assert (
        response.location
        == "https://conda.anaconda.org/conda-forge/linux-64/urllib3-1.25.3-py36_0.tar.bz2"
    )


def test_package_error(client, mocker, record_not_found):
    mocker.patch("conda.api.Solver.solve_final_state", side_effect=record_not_found)

    response = client.get(
        url_for("package", channel="anaconda", name="whoami", version="1.25.3"),
        follow_redirects=True,
    )
    data = json.loads(response.data)

    assert response.status == "404 NOT FOUND"
    assert data["error"] == 404
    assert data["text"] == "Error: Package(s) not found: \n  - whoami -> ==1.25.3"


def test_missing_parameter(client):
    response = client.get(url_for("package"), follow_redirects=True)
    data = json.loads(response.data)

    assert response.status == "404 NOT FOUND"
    assert data["error"] == 404
    assert data["text"] == "Error: Please provide a `name=` query parameter"
