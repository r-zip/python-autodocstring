from jsonrpcclient.clients.http_client import HTTPClient

from autodocstring.constants import DEFAULT_HOST, DEFAULT_PORT

if __name__ == "__main__":
    with open("autodocstring/autodocstring.py") as f:
        code = f.read()
    client = HTTPClient(f"http://{DEFAULT_HOST}:{DEFAULT_PORT}")
    result = client.request("get_docstring_info", source_code=code, line=29).data.result
    print(f"Received result: {result}")
