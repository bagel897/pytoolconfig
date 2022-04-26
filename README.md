# pytoolconfig
The goal of this project is to manage configuration for python tools, such as Black, rope, pylint, pytest, etc and add support for a pyproject.toml configuration file.
It will have several features:
 - [ ] Configuration file autodetection searching for the .git directory.
 - [ ] Universal keys
   - python minimum/maximum
   - line length
   - formatter ie: black
 - [ ] Global configuration
 - NO writing support, only reading
Support for 
- [ ] Pyproject.toml 
- [ ] Ini files 
- [ ] Tox.ini, setup.cfg
- [ ] config.py 
## Configuration Load Order
For example, black
1. pyproject.toml (mandatory, automatic) if tool.black (or your tool) is present
2. additional sources configured in order they were added.
3. global configuration from
 a) pytool.toml global file 
 b) configured global configurations
## Requirements
Depends on tomli for python < 3.11, tomllib for >=3.11. 
requires python >= 3.6
