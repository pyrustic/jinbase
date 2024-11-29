###### Jinbase API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/jinbase/__init__/README.md) | [Source](/src/jinbase/__init__.py)

# Class TypeRef
> Module: [jinbase.\_\_init\_\_](/docs/api/modules/jinbase/__init__/README.md)
>
> Class: **TypeRef**
>
> Inheritance: `object`

This class represents a mechanism for customizing
Python types allowed for (de)serializing data with Paradict classes and functions.
For example, one might want to only use Python OrderedDict instead of the regular
dict. In this case, just create a TypeRef instance, and make sure that you
set the dict_type attribute via the construction or a property.

```python
type_ref = TypeRef(dict_type=OrderedDict)
```

Still with this class, one could 'adapt' some exotic datatype so it will
conform with Python datatypes allowed in Paradict (de)serialization.
To do so, set the adapters attribute like this:

```python
adapters = {MyExoticType1: adapterFunction1, MyExoticType2: adapterFunction2}
type_ref = TypeRef(adapters=adapters)
```

## Properties table
Here are properties exposed in the class:

| Property | Methods | Description |
| --- | --- | --- |
| adapters | _getter, setter_ | No docstring. |
| bin\_type | _getter, setter_ | No docstring. |
| bin\_types | _getter, setter_ | No docstring. |
| bool\_type | _getter, setter_ | No docstring. |
| bool\_types | _getter, setter_ | No docstring. |
| complex\_type | _getter, setter_ | No docstring. |
| complex\_types | _getter, setter_ | No docstring. |
| date\_type | _getter, setter_ | No docstring. |
| date\_types | _getter, setter_ | No docstring. |
| datetime\_type | _getter, setter_ | No docstring. |
| datetime\_types | _getter, setter_ | No docstring. |
| dict\_type | _getter, setter_ | No docstring. |
| dict\_types | _getter, setter_ | No docstring. |
| float\_type | _getter, setter_ | No docstring. |
| float\_types | _getter, setter_ | No docstring. |
| grid\_type | _getter, setter_ | No docstring. |
| grid\_types | _getter, setter_ | No docstring. |
| int\_type | _getter, setter_ | No docstring. |
| int\_types | _getter, setter_ | No docstring. |
| list\_type | _getter, setter_ | No docstring. |
| list\_types | _getter, setter_ | No docstring. |
| obj\_type | _getter, setter_ | No docstring. |
| obj\_types | _getter, setter_ | No docstring. |
| set\_type | _getter, setter_ | No docstring. |
| set\_types | _getter, setter_ | No docstring. |
| str\_type | _getter, setter_ | No docstring. |
| str\_types | _getter, setter_ | No docstring. |
| time\_type | _getter, setter_ | No docstring. |
| time\_types | _getter, setter_ | No docstring. |

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

# Methods within class
Here are methods exposed in the class:
- [\_\_init\_\_](#__init__)
- [adapt](#adapt)
- [check](#check)
- [\_create\_map](#_create_map)
- [\_update\_types](#_update_types)

## \_\_init\_\_
Initialize self.  See help(type(self)) for accurate signature.

```python
def __init__(self, adapters=None, dict_type=None, list_type=None, set_type=None, obj_type=None, dict_types=None, list_types=None, set_types=None, obj_types=None, bin_type=None, bool_type=None, complex_type=None, date_type=None, datetime_type=None, float_type=None, grid_type=None, int_type=None, str_type=None, time_type=None, bin_types=None, bool_types=None, complex_types=None, date_types=None, datetime_types=None, float_types=None, grid_types=None, int_types=None, str_types=None, time_types=None):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## adapt
Checks the 'adapters' attribute to find out if there is
an adapter function registered for the type of the data argument.
Then, calls the adapter on the value.

```python
def adapt(self, value):
    ...
```

| Parameter | Description |
| --- | --- |
| value | the data value to adapt is an arbitrary Python object |

### Value to return
Returns the adapted value or the same value if no adapter is registered for its type

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## check
This function accepts as argument a Python type, and return
a Datatype instance if the type is supported/registered, else returns None

```python
def check(self, dtype):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## \_create\_map
No docstring

```python
def _create_map(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## \_update\_types
No docstring

```python
def _update_types(self, name, datatype):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>
