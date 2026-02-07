import pytest
import os
from dotenv import load_dotenv
from src.Verkada import VerkadaContext

INVALID_API_KEY="181w198w1ns9nnny9ecwe9c8ncw89n"
INVALID_VERKADA_URL="https://api.verkada.com/invalid"

instance = VerkadaContext()
cached_verkada_api_key: str
load_dotenv()

def test_Verkada_api_key_exists():
    verkada_api_key = os.environ.get("VERKADA_API_KEY", None)
    assert(verkada_api_key)
    global cached_verkada_api_key
    cached_verkada_api_key = verkada_api_key

def test_given_Verkada_api_key_exists():
    test_Verkada_api_key_exists()

def test_should_update_headers_after_successful_login(mocker):
    test_given_Verkada_api_key_exists()

    spy = mocker.spy(instance._session.headers, "update")
    instance.login(cached_verkada_api_key)

    spy.assert_called()

def test_should_exit_on_invalid_API_key():
    with pytest.raises(SystemExit) as e:
        instance.login(INVALID_API_KEY)
    assert(e.type == SystemExit)
    assert(e.value.code == 1)

def test_should_exit_on_invalid_endpoint_after_login():
    test_given_Verkada_api_key_exists()

    instance.login(cached_verkada_api_key)
    with pytest.raises(SystemExit) as e:
        instance._get(INVALID_VERKADA_URL)
    assert(e.type == SystemExit)
    assert(e.value.code == 1)
