from jinja2 import Environment, PackageLoader

DEFAULT_HOST: str = "localhost"  # the default host for the JSON RPC server
DEFAULT_PORT: int = 5000  # the default port for the JSON RPC server
TEMPLATE_ENV = Environment(loader=PackageLoader("autodocstring", "templates"))  # the Jinja environment for templates
