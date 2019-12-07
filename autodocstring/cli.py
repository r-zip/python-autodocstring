import json

import click

from .autodocstring import get_docstring_info
from .server import _start_server, _shutdown_server, get_matching_servers
from .constants import DEFAULT_HOST, DEFAULT_PORT


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "--host",
    type=str,
    default=DEFAULT_HOST,
    help=f"The host of the docstring generation server. Defaults to {DEFAULT_HOST}.",
)
@click.option(
    "--port",
    type=int,
    default=DEFAULT_PORT,
    help=f"The port of the docstring generation server. Defauts to {DEFAULT_PORT}.",
)
def start_server(host: str, port: int) -> None:
    servers = get_matching_servers(host, port)
    if len(servers) == 0:
        _start_server(host=host, port=port)
    else:
        click.echo(f"Server for host == {host}, port == {port} is already running.")


@click.command()
@click.option(
    "--host",
    type=str,
    default=DEFAULT_HOST,
    help=f"The host of the docstring generation server. Defaults to {DEFAULT_HOST}.",
)
@click.option(
    "--port",
    type=int,
    default=DEFAULT_PORT,
    help=f"The port of the docstring generation server. Defauts to {DEFAULT_PORT}.",
)
def shutdown_server(host: str, port: int) -> None:
    _shutdown_server(host, port)


@click.command()
@click.argument("uri", type=click.Path(file_okay=True, dir_okay=False, readable=True))
@click.argument("line", type=int)
def generate_docstring(uri: str, line: int) -> None:
    """Generate a single docstring for a function in the specified file."""
    docstring_info = get_docstring_info(uri, line)
    click.echo(json.dumps(docstring_info))


cli.add_command(start_server)
cli.add_command(shutdown_server)
cli.add_command(generate_docstring)

if __name__ == "__main__":
    cli()
