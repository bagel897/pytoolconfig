# Configuration
pytoolconfig supports the pyproject.toml configuration file
## pytoolconfig
| name                    | description                             | type   | default   | universal key                                              |
|-------------------------|-----------------------------------------|--------|-----------|------------------------------------------------------------|
| pytoolconfig.foo_other  | Tool One                                | str    | no        |                                                            |
| pytoolconfig.min_py_ver | This field is set via an universal key. | Tuple  |           | Mimimum target python version. Taken from requires-python. |
## pytoolconfig.subtool
| name                     | description   | type   | default   |
|--------------------------|---------------|--------|-----------|
| pytoolconfig.subtool.foo | foobar        | str    | lo        |
