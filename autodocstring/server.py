import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

from jsonrpcserver import dispatch, method

from .autodocstring import docstring_info
from .constants import DEFAULT_HOST, DEFAULT_PORT

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

docstring_info = method(docstring_info)


class AutodocstringHttpServer(BaseHTTPRequestHandler):
    def do_POST(self):
        # Process request
        request = self.rfile.read(int(self.headers["Content-Length"])).decode()
        logger.info(f"Received request: {request}")
        response = dispatch(request)
        # Return response
        self.send_response(response.http_status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(str(response).encode())


def start_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
    """Console script for python_autodocstring."""
    HTTPServer((host, port), AutodocstringHttpServer).serve_forever()
