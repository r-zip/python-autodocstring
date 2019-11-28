from jsonrpcclient.clients.http_client import HTTPClient

from autodocstring.constants import DEFAULT_HOST, DEFAULT_PORT

if __name__ == "__main__":
    client = HTTPClient(f"http://{DEFAULT_HOST}:{DEFAULT_PORT}")
    result = client.request("docstring_info", uri="autodocstring/autodocstring.py", line=29).data.result
    print(f"Received result: {result}")
