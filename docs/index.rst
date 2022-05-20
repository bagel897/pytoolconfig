.. pytoolconfig documentation master file, created by
   sphinx-quickstart on Fri May 13 15:23:25 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pytoolconfig's documentation!
========================================

Python Tool Configuration

The goal of this project is to manage configuration for python tools, such as black and rope and add support for a pyproject.toml configuration file. 

- Configuration file autodetection. (Searches for the .git and .hg directories (and others as configured)).
- :doc:`Optional global configuration <global_configuration>`
- :doc:`Optional command line overwrites <command_line>`
- :doc:`Optional Pydantic data validation and output. <pydantic>`
- :doc:`Universal Configuration keys <universal_config>`
- :doc:`Documentation Generation <generated/pytoolconfig.generate_documentation>`
- Read only support 

Configuration Sources 
---------------------
- :doc:`Pyproject.toml <generated/pytoolconfig.sources.pyproject>`
- :doc:`Ini files <generated/pytoolconfig.sources.ini>`
- :doc:`setup.cfg <generated/pytoolconfig.sources.setup_cfg>`
- :doc:`Command line arguments <command_line>`
- :doc:`Custom sources <generated/pytoolconfig.sources.source>`

Usage
-----
1. Define a pydantic model
2. Initialize pytoolconfig 
3. (Optional) Add custom configuration sources 
4. Parse configuration
5. (Optional) Generate schema.json and Configuration.md

Configuration Load Order
------------------------
0. Command Line - overwrites selected configuration properties individually
1. pyproject.toml (mandatory, automatic) if tool.black (or your tool) is present
2. additional sources configured in order they were added.
3. global configuration from pytool.toml global file 
4. configured global configurations

Contents
========
.. toctree::
   :maxdepth: 2

   command_line
   universal_config
   global_configuration
   pydantic
   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
