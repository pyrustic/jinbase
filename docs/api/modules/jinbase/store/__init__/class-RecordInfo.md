###### Jinbase API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/jinbase/store/__init__/README.md) | [Source](/src/jinbase/store/__init__.py)

# Class RecordInfo
> Module: [jinbase.store.\_\_init\_\_](/docs/api/modules/jinbase/store/__init__/README.md)
>
> Class: **RecordInfo**
>
> Inheritance: `tuple`

Named tuple returned by store.info()

## Fields table
Here are fields exposed in the class:

| Field | Description |
| --- | --- |
| uid | Alias for field number 0 |
| datatype | Alias for field number 1 |
| created\_at | Alias for field number 2 |

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

# Methods within class
Here are methods exposed in the class:
- [\_asdict](#_asdict)
- [\_make](#_make)
- [\_replace](#_replace)

## \_asdict
Return a new dict which maps field names to their values.

```python
def _asdict(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## \_make
Make a new RecordInfo object from a sequence or iterable

```python
@classmethod
def _make(iterable):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## \_replace
Return a new RecordInfo object replacing specified fields with new values

```python
def _replace(self, /, **kwds):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>
