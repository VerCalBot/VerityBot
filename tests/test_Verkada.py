import pytest
import os
from dotenv import load_dotenv
from typing import Callable, Any
from src.Verkada import VerkadaContext

INVALID_API_KEY="181w198w1ns9nnny9ecwe9c8ncw89n"
INVALID_VERKADA_URL="https://api.verkada.com/invalid"

instance = VerkadaContext()
cached_verkada_api_key: str
load_dotenv()


# helpers
def Verkada_api_key_exists():
    verkada_api_key = os.environ.get("VERKADA_API_KEY", None)
    assert(verkada_api_key)
    global cached_verkada_api_key
    cached_verkada_api_key = verkada_api_key

def higher_order_sysexit_handler(f: Callable[[str], Any], arg: str) -> None:
    with pytest.raises(SystemExit) as e:
        f(arg)
    assert(e.type == SystemExit)
    assert(e.value.code == 1)

# tests
def test_given_Verkada_api_key_exists():
    Verkada_api_key_exists()

def test_should_update_headers_after_successful_login(mocker):
    test_given_Verkada_api_key_exists()

    spy = mocker.spy(instance._session.headers, "update")
    instance.login(cached_verkada_api_key)

    spy.assert_called()

def test_should_exit_on_invalid_API_key():
    higher_order_sysexit_handler(instance.login, INVALID_API_KEY)

def test_should_exit_on_invalid_endpoint_after_login():
    test_given_Verkada_api_key_exists()

    higher_order_sysexit_handler(instance._get, INVALID_VERKADA_URL)
