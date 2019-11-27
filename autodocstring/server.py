from http.server import HTTPServer

from .autodocstring import TestHttpServer


def start_server():
    """Console script for python_autodocstring."""
    HTTPServer(("localhost", 5000), TestHttpServer).serve_forever()
