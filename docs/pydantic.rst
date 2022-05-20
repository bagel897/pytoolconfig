Pydantic
========

PyToolConfig supports optional pydantic validation.
To use it, install pytoolconfig with the validation extra.
Then, use the pydantic dataclass decorator instead of the standard library one.
Additionally, pytoolconfig provides its own dataclass decorator, which is the pydantic one when available and the standard one when not.

Fields
------
Furthermore, you can now use pydantic fields instead of pytoolconfig fields. This will allow for you to add validators and other features into the fields.
