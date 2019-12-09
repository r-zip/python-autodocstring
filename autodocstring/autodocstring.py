from itertools import dropwhile, takewhile
from typing import Any, Dict, List, Optional
from uuid import uuid4

import parso
from parso.python.tree import ClassOrFunc, Function, Module


def get_parse_tree(uri: str) -> Module:
    """
    Load the parse tree for a Python file.

    Args:
        uri (str): The path to the Python file.

    Returns:
        Module: The Python module, as parsed by Parso.
    """
    with open(uri) as f:
        code = f.read()

    return parso.parse(code)


def get_toplevel_defs(uri: str) -> List[ClassOrFunc]:
    """
    Load the top-level class and function definitions for the file.

    Args:
        uri (str): The path to the Python file.

    Returns:
        List[ClassOrFunc]: A list of class and function definitions for uri.
    """
    tree = get_parse_tree(uri)
    return [*tree.iter_funcdefs(), *tree.iter_classdefs()]


def get_enclosing_defn(uri: str, line: int, defs: List[ClassOrFunc]) -> Optional[ClassOrFunc]:
    """
    Recursively search for the most nested class or function definition at the specified line in the file uri.

    Args:
        uri (str): The path to the Python file.
        line (int): The line in the file given by uri for which to find the definition.
        defs (List[ClassOrFunc]): A list of candidate definitions for the line and file.

    Returns:
        Optional[ClassOrFunc]: The most nested function or class definition, if there is one at the given line and
            file, else None.
    """
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
    """
    Get the docstring context information for the given file (uri) and line (line). Return the result as a dictionary
    for JSON serialization. If no suitable definition is found, return None.

    The schema of the docstring information is as follows:
    {
        "func_name": <str>,
        "params": [
            {"name": <str>, "annotation": <str>, "default": <str>},
            ...
        ],
        "return_typehint": <str>,
        "raise_types": [<str>, ...],
        "id": <str>,
    }

    Args:
        uri (str): The path to the Python file.
        line (int): The line in the file given by uri for which to find the definition.

    Returns:
        Optional[Dict[str, Any]]: The docstring information dictionary for the function at the given line in the file
            specified by uri.
    """
    toplevel_defs = get_toplevel_defs(uri)
    enclosing_defn = get_enclosing_defn(uri, line, toplevel_defs)
    if enclosing_defn is None:
        return None

    if type(enclosing_defn) == Function:
        return get_function_info(enclosing_defn)

    return None


def get_function_info(defn: Function) -> Dict[str, Any]:
    """
    Extract docstring information for the given function.

    Args:
        defn (Function): The function of interest.

    Returns:
        Dict[str, Any]: The docstring information for the given defun.
    """
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
    """
    Reconstruct code for the given node, and strip it of whitespace.

    Args:
        node (Any): An object representing a node of the Parso abstract syntax tree.

    Returns:
        str: The string representation of the abstract syntax tree node.
    """
    if node is None:
        return None
    return node.get_code().strip()


def is_arrow(node: Any) -> bool:
    """
    Predicate that tests whether the given AST node matches '->'.

    Args:
        node (Any): An object representing a node of the Parso abstract syntax tree.

    Returns:
        bool: Whether node represents the token '->'.
    """
    return node.type == "operator" and node.value == "->"


def is_colon(node: Any) -> bool:
    """
    Predicate that tests whether the given AST node matches ':'.

    Args:
        node (Any): An object representing a node of the Parso abstract syntax tree.

    Returns:
        bool: Whether node represents the token ':'.
    """
    return node.type == "operator" and node.value == ":"
