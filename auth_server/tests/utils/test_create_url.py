from auth_server.utils.create_url import create_url_for_email


def test_create_url_for_email_http():
    use_https = False
    hostname = "localtest.me"
    path = "/test"
    query = {"test_key": "test_value"}
    url = create_url_for_email(use_https, hostname, path, query)
    assert "http://localtest.me/test?test_key=test_value" == url


def test_create_url_for_email_https():
    use_https = True
    hostname = "localtest.me"
    path = "/test"
    query = {"test_key": "test_value"}
    url = create_url_for_email(use_https, hostname, path, query)
    assert "https://localtest.me/test?test_key=test_value" == url
