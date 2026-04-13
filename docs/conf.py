import os
import sys

# Add the src directory to the Python path for autodoc
sys.path.insert(0, os.path.abspath("../src"))

project = "wclickhouse"
copyright = "2026, William Steve Rodriguez Villamizar"
author = "William Steve Rodriguez Villamizar"
release = "0.1.0"
version = "0.1"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx.ext.todo",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"
html_title = "wclickhouse Documentation"

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": False,
    "show-inheritance": True,
}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest", None),
}

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

language = "en"
