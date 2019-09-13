import io
import json

import pytest

from flask import url_for


def test_index(client):
    """ Sanity check """
    assert client.get(url_for("index")).status_code == 200


def _post_multipart(client, name, view="parse"):
    with open(name, "rb") as all_styles:
        data = {"file": (io.BytesIO(all_styles.read()), name)}

    return client.post(
        url_for(view),
        data=data,
        follow_redirects=True,
        content_type="multipart/form-data",
    )


def _post_urlencoded(client, name, view="parse"):
    with open(name, "rb") as all_styles:
        data = {"file": all_styles.read(), "filename": name}

    return client.post(
        url_for(view),
        data=data,
        follow_redirects=True,
        content_type="application/x-www-form-urlencoded",
    )


def test_parse_file(client, mocker, fake_numpy_deps):
    """ testing parsing POST """
    mocker.patch("conda.api.Solver.solve_final_state", side_effect=fake_numpy_deps)

    response = _post_urlencoded(client, "tests/fixtures/just_numpy.yml", "parse")
    assert response.status == "200 OK"

    response = _post_multipart(client, "tests/fixtures/just_numpy.yml", "parse")

    assert response.status == "200 OK"

    data = json.loads(response.data)

    assert data["channels"] == ["anaconda"]
    assert {"name": "numpy-base", "requirement": "1.16.4"} in data["lockfile"]


def test_parse_file_not_found(client, mocker, record_not_found):
    """ testing parsing POST """
    mocker.patch("conda.api.Solver.solve_final_state", side_effect=record_not_found)

    response = _post_urlencoded(client, "tests/fixtures/just_numpy.yml", "parse")
    assert response.status == "404 NOT FOUND"
    assert json.loads(response.data) == {
        "error": 404,
        "text": "Error: Package(s) not found: \n  - whoami -> ==1.25.3",
    }


def test_info(client, mocker, solved_urllib3, expected_result_urllib3):
    mocker.patch("conda.api.Solver.solve_final_state", side_effect=solved_urllib3)

    # name and channel
    response = client.get(
        url_for("info", channel="anaconda", package="urllib3"), follow_redirects=True
    )
    assert response.status == "200 OK"
    data = json.loads(response.data)

    assert data["license"] == "MIT"

    # all parameters
    response = client.get(
        url_for("info", channel="anaconda", package="urllib3", version="==1.25.3"),
        follow_redirects=True,
    )
    assert response.status == "200 OK"
    data = json.loads(response.data)

    assert data == expected_result_urllib3

    # urlencoded
    response = client.get(
        url_for("info", channel="pkgs%3Dmain", package="urllib3", version="==1.25.3"),
        follow_redirects=True,
    )
    assert response.status == "200 OK"
    data = json.loads(response.data)

    assert data == expected_result_urllib3



def test_info_error(client, mocker, record_not_found):
    mocker.patch("conda.api.Solver.solve_final_state", side_effect=record_not_found)

    response = client.get(
        url_for("info", channel="anaconda", package="whoami", version="==1.25.3"),
        follow_redirects=True,
    )
    data = json.loads(response.data)

    assert response.status == "404 NOT FOUND"
    assert data["error"] == 404
    assert data["text"] == "Error: Package(s) not found: \n  - whoami -> ==1.25.3"
