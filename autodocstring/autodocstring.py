from typing import Dict, List

import parso
from parso.python.tree import ClassOrFunc, Module


class Foo:
    def __init__(self):
        pass

    def bar(self):
        pass


def get_parse_tree(uri: str) -> Module:
    with open(uri) as f:
        code = f.read()

    return parso.parse(code)


def get_toplevel_defs(uri: str) -> Dict:
    tree = get_parse_tree(uri)
    toplevel_funcdefs = list(tree.iter_funcdefs())
    toplevel_classdefs = list(tree.iter_classdefs())
    return [*toplevel_funcdefs, *toplevel_classdefs]


def get_enclosing_def(uri: str, line: int, defs: List) -> ClassOrFunc:
    # base cases
    if len(defs) == 0:
        return None

    for def_ in defs:
        if isinstance(def_, ClassOrFunc) and def_.start_pos[0] <= line and def_.end_pos[0] >= line:
            nested_defs = list(def_.iter_funcdefs()) + list(def_.iter_classdefs())
            return get_enclosing_def(uri, line, nested_defs) or def_

    return None


if __name__ == "__main__":
    uri = "autodocstring/autodocstring.py"
    line = 39
    toplevel_defs = get_toplevel_defs(uri)
    enclosing_funcdef = get_enclosing_def(uri, line, toplevel_defs)
