from itertools import dropwhile, takewhile
from uuid import uuid4
from typing import Any, Dict, List

import parso
from parso.python.tree import Function


class Interval:
    def __init__(self, low: float, high: float):
        self.low = low
        self.high = high

    def contains(self, other: "Interval") -> bool:
        if other.low <= self.low and self.high <= other.high:
            return True
        return False

    def overlaps_with(self, other: "Interval") -> bool:
        if self.high <= other.low or self.low >= other.high:
            return True
        return False


def get_funcdefs_at_point(uri: str, current_line: int, innermost: bool = True) -> List[Function]:
    with open(uri) as f:
        code = f.read()
    tree = parso.parse(code)
    funcdefs = list(tree.iter_funcdefs())
    funcdefs_at_point = []

    for funcdef in funcdefs:
        if funcdef.start_pos[0] <= current_line <= funcdef.end_pos[0]:
            funcdefs_at_point.append(funcdef)

    return funcdefs_at_point


def to_code(node: Any) -> str:
    if node is None:
        return None
    return node.get_code().strip()


def is_arrow(node: Any) -> str:
    return node.type == "operator" and node.value == "->"


def is_colon(node: Any) -> str:
    return node.type == "operator" and node.value == ":"


# TODO: get outermost or innermost docstring
def docstring_info(uri: str, line: int) -> Dict:
    # if there are no function definitions at the current line, return None
    funcdef = get_funcdefs_at_point(uri, line)[0]
    if funcdef is None:
        return None

    # get the function name, parameters, and return typehint
    func_name = funcdef.name.value
    # TODO: don't let nested definitions pollute these lists
    parameters = [node for node in funcdef.children if node.type == "parameters"][0]
    params = [p for p in parameters.children if p.type == "param"]

    return_typehint = None
    # if there's a return typehint, get it
    if any(is_arrow(n) for n in funcdef.children) and any(is_arrow(n) for n in funcdef.children):
        # take only the stuff between the arrow and the colon
        children = dropwhile(lambda x: not is_arrow(x), funcdef.children)
        children = list(takewhile(lambda x: not is_colon(x), children))
        if len(children) == 2:
            return_typehint = to_code(list(children)[1])

    # return the response as a dictionary
    response = {
        "func_name": func_name,
        "params": [
            {"name": p.name.value, "annotation": to_code(p.annotation), "default": to_code(p.default)} for p in params
        ],
        "return_typehint": return_typehint,
        "id": str(uuid4()),
    }

    return response


if __name__ == "__main__":
    docstring_info("autodocstring/autodocstring.py", 67)
