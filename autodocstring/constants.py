from jinja2 import Environment, PackageLoader

DEFAULT_HOST: str = "localhost"
DEFAULT_PORT: int = 5000
TEMPLATE_ENV = Environment(loader=PackageLoader("autodocstring", "templates"))
