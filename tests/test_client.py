import pytest
import requests_mock
from leakix import Client, SuccessResponse
from l9format import l9format
from pathlib import Path
import os
import json

RESULTS_DIR = Path(os.path.dirname(__file__)) / "results"
HOSTS_RESULTS_DIR = RESULTS_DIR / "host"
HOSTS_SUCCESS_RESULTS_DIR = HOSTS_RESULTS_DIR / "success"
HOSTS_404_RESULTS_DIR = HOSTS_RESULTS_DIR / "404"


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def fake_ipv4():
    return "33.33.33.33"


def test_get_host_success(client):
    for f in Path.iterdir(HOSTS_SUCCESS_RESULTS_DIR):
        filename = f.name
        with open(str(f), "r") as ff:
            res_json = json.load(ff)
        # remove .json
        ipv4 = f.name[:-5]
        with requests_mock.Mocker() as m:
            url = "%s/host/%s" % (client.BASE_URL, ipv4)
            m.get(url, json=res_json, status_code=200)
            response = client.get_host(ipv4)
            assert response.is_success()
            assert len(response.json()["services"]) == 3
            assert response.json()["leaks"] is None


def test_get_host_404(client):
    for f in Path.iterdir(HOSTS_404_RESULTS_DIR):
        filename = f.name
        with open(str(f), "r") as ff:
            res_json = json.load(ff)
        # remove .json
        ipv4 = f.name[:-5]
        client = Client()
        with requests_mock.Mocker() as m:
            url = "%s/host/%s" % (client.BASE_URL, ipv4)
            m.get(url, json=res_json, status_code=404)
            response = client.get_host(ipv4)
            assert response.is_error()
            assert response.status_code() == 404
            assert response.json()["title"] == "Not Found"
            assert response.json()["description"] == "Host not found"


def test_get_host_429(client, fake_ipv4):
    status_code = 429
    res_json = {"reason": "rate-limit", "status": "error"}
    with requests_mock.Mocker() as m:
        url = "%s/host/%s" % (client.BASE_URL, fake_ipv4)
        m.get(url, json=res_json, status_code=status_code)
        response = client.get_host(fake_ipv4)
        assert response.is_error()
        assert response.status_code() == status_code
        assert response.json() == res_json
