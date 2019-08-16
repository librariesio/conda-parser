import io
import json

import pytest

from flask import url_for


def test_index(client):
    """ Sanity check """
    assert client.get(url_for("index")).status_code == 200


def _post_file(client, name, view="parse"):
    with open(name, "rb") as all_styles:
        data = {"file": (io.BytesIO(all_styles.read()), name)}

    return client.post(
        url_for(view),
        data=data,
        follow_redirects=True,
        content_type="multipart/form-data",
    )


def test_parse(client, mocker, fake_numpy_deps):
    """ testing parsing POST """
    mocker.patch("conda.api.Solver.solve_final_state", side_effect=fake_numpy_deps)

    response = _post_file(client, "tests/fixtures/just_numpy.yml", "parse")

    assert response.status == "200 OK"

    data = json.loads(response.data)

    assert data["channels"] == ["anaconda"]
    assert {"name": "numpy-base", "requirement": "1.16.4"} in data["dependencies"]
