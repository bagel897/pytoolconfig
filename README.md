# Pytoolconfig
**Py**thon **Tool** **Config**uration

The goal of this project is to manage configuration for python tools, such as black and rope and add support for a pyproject.toml configuration file. 
 - Configuration file autodetection searching for the .git directory (and others as configured).
 - Optional global configuration
 - Optional command line overwrites
 - Pydantic data validation and output.
 - Get minimum target python version
 - Read only support 
 
Support for 
- Pyproject.toml 
- Ini files
- setup.cfg 
- tox.ini (via Ini Files)
- Command line arguments
- Custom sources 

## Usage:
1. Define a pydantic model
2. Initialize pytoolconfig 
3. (Optional) Add custom configuration sources 
4. Parse configuration
5. (Optional) Generate schema.json and Configuration.md

## Configuration Load Order
0. Command Line - overwrites selected configuration properties individually
1. pyproject.toml (mandatory, automatic) if tool.black (or your tool) is present
2. additional sources configured in order they were added.
3. global configuration from
 a) pytool.toml global file 
 b) configured global configurations

## Command Line Overwrites:
1. In the Configuration Model, set the ```command_line``` value in the `Field` constructor. (This only works for items in the base model)
For example:
```py 
class nestedmodel(basemodel):
    foo_other: str = field(description="w", default="no", command_line=("--foo", "-f"))
```
2. Pass an Argument Parser to the ```PyToolConfig``` constructor
3. (Optional) Pass arguments to the ```parse()``` command

## Global Configuration
1. Install with the ``global`` extra, like ```pip install pytoolconfig[global]```
2. Pass an array of global sources to the PyToolConfig constructor. PyToolConfig will add a pytool.toml file first if the global_config option is passed.
3. Parse as usual

## Universal Keys
In your configuration model, set the ```universal_config``` value in the `Field constructor`. (This only works for items in the base model). You still need to set a default value.
For example:
```py 
class nestedmodel(basemodel):
    foo_other: str = field(description="w", default="no", universal_config=("min_py_version"))
```
The value of this field will be overwritten by pytoolconfig's equivalent universal configuration field.
## Documentation Generation
Refer to the documentation function in pytoolconfig
## Goals
- [ ] Configuration document generation
- [x] Universal keys
