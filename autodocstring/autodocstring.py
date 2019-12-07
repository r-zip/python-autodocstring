from itertools import dropwhile, takewhile
from typing import Any, Dict, List, Optional
from uuid import uuid4

import parso
from parso.python.tree import ClassOrFunc, Function, Module


def get_parse_tree(uri: str) -> Module:
    with open(uri) as f:
        code = f.read()

    return parso.parse(code)


def get_toplevel_defs(uri: str) -> Dict:
    tree = get_parse_tree(uri)
    return [*tree.iter_funcdefs(), *tree.iter_classdefs()]


def get_enclosing_defn(uri: str, line: int, defs: List[ClassOrFunc]) -> Optional[ClassOrFunc]:
    # base case
    if len(defs) == 0:
        return None

    # recursion
    for defn in defs:
        if isinstance(defn, ClassOrFunc) and defn.start_pos[0] <= line and defn.end_pos[0] >= line:
            # search over this definition's function and class definitions
            nested_defs = [*defn.iter_funcdefs(), *defn.iter_classdefs()]
            # prefer most nested def
            return get_enclosing_defn(uri, line, nested_defs) or defn

    return None


def get_docstring_info(uri: str, line: int) -> Optional[Dict[str, Any]]:
    toplevel_defs = get_toplevel_defs(uri)
    enclosing_defn = get_enclosing_defn(uri, line, toplevel_defs)
    if enclosing_defn is None:
        return None

    if type(enclosing_defn) == Function:
        return get_function_info(enclosing_defn)

    return None


def get_function_info(defn: Function) -> Dict[str, Any]:
    parameters = [node for node in defn.children if node.type == "parameters"][0]
    params = [p for p in parameters.children if p.type == "param"]

    return_typehint = None
    # if there's a return typehint, get it
    if any(is_arrow(n) for n in defn.children) and any(is_colon(n) for n in defn.children):
        # take only the stuff between the arrow and the colon
        children = dropwhile(lambda x: not is_arrow(x), defn.children)
        children = list(takewhile(lambda x: not is_colon(x), children))
        if len(children) == 2:
            return_typehint = to_code(list(children)[1])

    raise_types = [to_code(stmt.children[1].children[0]) for stmt in defn.iter_raise_stmts()]

    return {
        "func_name": defn.name.value,
        "params": [
            {"name": p.name.value, "annotation": to_code(p.annotation), "default": to_code(p.default)} for p in params
        ],
        "return_typehint": return_typehint,
        "raise_types": raise_types,
        "id": str(uuid4()),
    }


def to_code(node: Any) -> str:
    if node is None:
        return None
    return node.get_code().strip()


def is_arrow(node: Any) -> str:
    return node.type == "operator" and node.value == "->"


def is_colon(node: Any) -> str:
    return node.type == "operator" and node.value == ":"
