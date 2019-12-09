import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import List, Dict

from jsonrpcserver import dispatch, method

from .autodocstring import get_docstring_info
from .constants import DEFAULT_HOST, DEFAULT_PORT

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

docstring_info = method(get_docstring_info)

SERVERS: List[Dict] = []


class AutodocstringHttpServer(BaseHTTPRequestHandler):
    """
    A JSON RPC server capable of parsing Python docstrings.
    """

    def do_POST(self) -> None:
        """
        Handle an HTTP POST. The encoded request is handled by jsonrpcserver.dispatch.
        """
        # Process request
        request = self.rfile.read(int(self.headers["Content-Length"])).decode()
        logger.info(f"Received request: {request}")
        response = dispatch(request)
        # Return response
        self.send_response(response.http_status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(str(response).encode())


def get_matching_servers(host: str, port: int) -> List[Dict]:
    """
    Get a list of running servers matching the given host and port combination.

    Args:
        host (str): The host of the server.
        port (int): The port of  the server.

    Returns:
        List[Dict]: A list of servers as dictionaries, with the server itself, host, and port for each server.
    """
    matching_servers = [s for s in SERVERS if s["host"] == host and s["port"] == port]
    return matching_servers


def _start_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    """
    Start a server on the given host and port, if none exists.

    Args:
        host (str): The host of the server.
        port (int): The port of  the server.

    Raises:
        ValueError: If a server is already running on the specified host and port.
    """
    if len(get_matching_servers(host, port)) > 0:
        raise ValueError(f"Server already running for host {host}, port {port}!")

    server = HTTPServer((host, port), AutodocstringHttpServer)
    SERVERS.append({"server": server, "host": host, "port": port})
    try:
        server.serve_forever()
    except Exception:
        server.shutdown()


def _shutdown_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    """
    Shut down server for the given host and port, if it exists.

    Args:
        host (str): The host of the server.
        port (int): The port of  the server.

    Raises:
        ValueError: If there are no servers running on the specified host on the specified port.
        ValueError: If there is more than one server matching the host and port (this should not happen).
    """
    matching_servers = get_matching_servers(host, port)
    if len(matching_servers) == 1:
        server = matching_servers[0]
        server.shutdown()
    elif len(matching_servers) == 0:
        raise ValueError(f"Could not find servers matching host == {host} and port == {port}.")
    else:
        raise ValueError(f"Found multiple servers matching host == {host} and port == {port}.")
