from jsonrpcclient.clients.http_client import HTTPClient

from .constants import HOST, DEFAULT_PORT

if __name__ == "__main__":
    client = HTTPClient(f"http://{HOST}:{DEFAULT_PORT}")
    result = client.request("docstring_info", uri="autodocstring/autodocstring.py", line=15).data.result
    print(f"Received result: {result}")
