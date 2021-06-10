from typing import Dict
from urllib.parse import urlencode, urlunparse


def create_url_for_email(use_https: bool,
                         hostname: str,
                         path: str,
                         query: Dict[str, str]) -> str:
    if use_https:
        scheme = "https"
    else:
        scheme = "http"

    return urlunparse((scheme, hostname, path, '', urlencode(query), ''))
