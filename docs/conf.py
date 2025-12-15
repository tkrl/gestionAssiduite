# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import django

sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../../teamProject'))

# Configuration Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'teamProject.settings'
django.setup()

project = 'gestionAssiduite'
copyright = '2025, Longin & Cie'
author = 'Longin & Cie'
release = 'getionAssiduite'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Thème
html_theme = 'sphinx_rtd_theme'

# Internationalisation
language = 'fr'

# Configuration autodoc
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Pour inclure les docstrings Google/NumPy
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
html_static_path = ['_static']

# Configuration Sphinx
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinx_rtd_theme',
    'myst_parser',
     'sphinxcontrib.mermaid',
]

master_doc = 'source/index'  # Si vous voulez le garder dans source/

