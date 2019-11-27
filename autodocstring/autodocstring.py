# -*- coding: utf-8 -*-

"""Main module."""
from http.server import BaseHTTPRequestHandler

import parso
from parso.python.tree import Module
from jsonrpcserver import method, dispatch


@method
def ping():
    return "pong"


# TODO: allow no line_start/line_stop
def get_file_contents(uri: str, line_start: int, line_stop: int) -> str:
    contents = ""
    with open(uri) as f:
        for _ in range(line_start):
            f.readline()
        for _ in range(line_stop - line_start):
            contents += f.readline()
    return contents


# TODO: allow no line_start/line_stop
def get_funcdef(uri: str, line_start: int, line_stop: int, current_line=None):
    if (current_line is not None) and not (line_start <= current_line <= line_stop):
        raise ValueError("Current line must be between starting and ending lines.")
    if current_line:
        with open(uri) as f:
            code = f.read()
        tree = parso.parse(code)
        funcdefs = list(tree.iter_funcdefs())
        for funcdef in funcdefs:
            pass
    else:
        code = get_file_contents(uri, line_start, line_stop)
        tree = parso.parse(code)
        funcdefs = list(tree.iter_funcdefs())
        if len(funcdefs) == 0:
            return None
        else:
            funcdef = funcdefs[0]
    return funcdef


def get_code(node):
    if node is None:
        return None
    return node.get_code().strip()


def docstring(uri: str, line_start: int, line_stop: int, current_line: int = None) -> Module:
    funcdef = get_funcdef(uri, line_start, line_stop, current_line)
    if funcdef is None:
        return None
    func_name = funcdef.name.value
    try:
        parameters = [node for node in funcdef.children if node.type == "parameters"][0]
    except IndexError:
        raise ValueError("Couldn't find parameters.")
    params = [p for p in parameters.children if p.type == "param"]
    return {
        "func_name": func_name,
        "params": [
            {"name": p.name.value, "annotation": get_code(p.annotation), "default": get_code(p.default)} for p in params
        ],
    }


class TestHttpServer(BaseHTTPRequestHandler):
    def do_POST(self):
        # Process request
        request = self.rfile.read(int(self.headers["Content-Length"])).decode()
        response = dispatch(request)
        # Return response
        self.send_response(response.http_status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(str(response).encode())
