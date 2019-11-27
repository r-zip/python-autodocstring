# -*- coding: utf-8 -*-

"""Console script for python_autodocstring."""
import sys

from .server import start_server


def main():
    start_server()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
