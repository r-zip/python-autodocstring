# -*- coding: utf-8 -*-

"""Main module."""
from http.server import BaseHTTPRequestHandler
from itertools import dropwhile, takewhile
from typing import Union

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


def get_funcdef_at_point(uri: str, current_line: int):
    with open(uri) as f:
        code = f.read()
    tree = parso.parse(code)
    funcdefs = list(tree.iter_funcdefs())
    current_funcdef = None
    for funcdef in funcdefs:
        if funcdef.start_pos[0] <= current_line <= funcdef.end_pos[0]:
            current_funcdef = funcdef
    return current_funcdef


def get_code(node):
    if node is None:
        return None
    return node.get_code().strip()


def is_arrow(node):
    return node.type == "operator" and node.value == "->"


def is_colon(node):
    return node.type == "operator" and node.value == ":"


def is_name(node):
    pass


def docstring(uri: str, current_line: int = None) -> Union[Module, str]:
    funcdef = get_funcdef_at_point(uri, current_line)
    if funcdef is None:
        return None
    func_name = funcdef.name.value
    parameters = [node for node in funcdef.children if node.type == "parameters"][0]
    params = [p for p in parameters.children if p.type == "param"]
    if any(is_arrow(n) for n in funcdef.children) and any(is_arrow(n) for n in funcdef.children):
        children = dropwhile(lambda x: not is_arrow(x), funcdef.children)
        children = takewhile(lambda x: not is_colon(x), children)
        return_typehint = get_code(list(children)[1])
    return {
        "func_name": func_name,
        "params": [
            {"name": p.name.value, "annotation": get_code(p.annotation), "default": get_code(p.default)} for p in params
        ],
        "return_typehint": return_typehint,
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
