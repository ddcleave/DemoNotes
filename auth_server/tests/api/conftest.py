import pytest
from requests.sessions import session
from auth_server.core.config import get_settings
from requests import Session


@pytest.fixture(scope="session")
def url():
    return "http://" + get_settings().domain


@pytest.fixture
def maildev():
    with Session() as em:
        em.delete("http://" + get_settings().test_mail_server +
                  ":1080/email/all")
        yield
        em.delete("http://" + get_settings().test_mail_server +
                  ":1080/email/all")
