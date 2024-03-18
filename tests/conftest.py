from unittest.mock import patch

import pytest
from invenio_app.factory import create_api as _create_api

from invenio_fts.manager import TransferManager


@pytest.fixture(scope="module")
def create_app(instance_path, entry_points):
    """Application factory fixture."""
    return _create_api


def blabla(self):
    return {"url": "test", "api": {"major": 2, "minor": 2, "patch": 3}}


@pytest.fixture()
def ftsmanager():
    print("Fixture for the manager")
    endpoint = "https://fts3-public.cern.ch:8446"
    ucert = ""

    ukey = ""
    with patch("fts3.rest.client.context.Context._validate_endpoint", blabla):
        fts = TransferManager(endpoint, ucert, ukey)
    return fts
