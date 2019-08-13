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


def test_parse(client):
    """ testing parsing POST """
    response = _post_file(client, "tests/fixtures/just_numpy.yml", "parse")
    assert response.status == "200 OK"
    assert json.loads(response.data)["channels"] == ["anaconda"]
    assert json.loads(response.data)["dependencies"] == [
        {"name": "numpy", "requirement": ">= 0"}
    ]


def test_parse_v10(client):
    """ testing parsing POST """
    response = _post_file(client, "tests/fixtures/just_numpy.yml", "parse_v10")
    assert response.status == "200 OK"
    assert json.loads(response.data)["channels"] == ["anaconda"]
    assert json.loads(response.data)["dependencies"] == [
        {"name": "numpy", "requirement": ">= 0"}
    ]
