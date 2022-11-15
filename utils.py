import http.client
import urllib.request


def send_http_request(url: str, data: bytes) -> http.client.HTTPResponse:
    return urllib.request.urlopen(url, data)
