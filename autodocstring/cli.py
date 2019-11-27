# -*- coding: utf-8 -*-

"""Console script for python_autodocstring."""
import sys
import argparse

from .server import start_server
from .constants import DEFAULT_HOST, DEFAULT_PORT


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host",
        required=False,
        default=DEFAULT_HOST,
        help=f"The host of the docstring generation server. Defaults to {DEFAULT_HOST}.",
    )
    parser.add_argument(
        "--port",
        required=False,
        default=DEFAULT_PORT,
        help=f"The port of the docstring generation server. Defauts to {DEFAULT_PORT}.",
    )
    arguments = parser.parse_args()
    host = arguments.host
    port = arguments.port
    start_server(host=host, port=port)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
