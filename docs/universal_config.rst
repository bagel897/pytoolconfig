Universal Config 
================
Universal Configuration refers to keys given by pytoolconfig. You can overwrite your own configuration keys with the ones provided by pytoolconfig.

In your configuration model, set the ``universal_config`` value in the `Field` constructor. (This only works for items in the base model). You still need to set a default value.
For example:

.. code-block:: python

    @dataclass
    class NestedModel:
        foo_other: str = Field(
            description="w", default="no", universal_config=("min_py_version")
        )

The value of this field will be overwritten by pytoolconfig's equivalent universal configuration field.
