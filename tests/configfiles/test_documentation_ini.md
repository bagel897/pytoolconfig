# Configuration
pytoolconfig supports the following configuration files
 1. pyproject.toml
 2. setup.cfg
 3. pytool.toml
## pytoolconfig
| name                    | description                             | type   | default   | universal key                                              | command line flag   |
|-------------------------|-----------------------------------------|--------|-----------|------------------------------------------------------------|---------------------|
| pytoolconfig.foo_other  | Tool One                                | str    | no        |                                                            | --foo, -f           |
| pytoolconfig.min_py_ver | This field is set via an universal key. | Tuple  |           | Mimimum target python version. Taken from requires-python. |                     |
## pytoolconfig.subtool
| name                     | description   | type   | default   |
|--------------------------|---------------|--------|-----------|
| pytoolconfig.subtool.foo | foobar        | str    | lo        |
