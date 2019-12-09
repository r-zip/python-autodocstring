from jsonrpcclient.clients.http_client import HTTPClient

from autodocstring.constants import DEFAULT_HOST, DEFAULT_PORT
from autodocstring.server import _start_server, _shutdown_server

if __name__ == "__main__":
    client = HTTPClient(f"http://{DEFAULT_HOST}:{DEFAULT_PORT}")
    result = client.request("get_docstring_info", uri="autodocstring/autodocstring.py", line=29).data.result
    print(f"Received result: {result}")
