###### Jinbase API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/jinbase/store/depot/README.md) | [Source](/src/jinbase/store/depot.py)

# Class Depot
> Module: [jinbase.store.depot](/docs/api/modules/jinbase/store/depot/README.md)
>
> Class: **Depot**
>
> Inheritance: [jinbase.store.Store](/docs/api/modules/jinbase/store/class-Store.md)

This class represents the Depot store.
Note that a Depot object isn't intended to be directly
instantiated by the user.

## Fields table
Here are fields exposed in the class:

| Field | Value |
| --- | --- |
| \_abc\_impl | `<_abc._abc_data object at 0x789010e44100>` |

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## Properties table
Here are properties exposed in the class:

| Property | Methods | Description |
| --- | --- | --- |
| chunk\_size | _getter_ | No docstring. |
| dbc | _getter_ | No docstring. |
| filename | _getter_ | No docstring. |
| in\_memory | _getter_ | No docstring. |
| is\_closed | _getter_ | No docstring. |
| is\_new | _getter_ | No docstring. |
| is\_readonly | _getter_ | No docstring. |
| jinbase | _getter_ | No docstring. |
| model | _getter_ | No docstring. |
| timeout | _getter_ | No docstring. |
| type\_ref | _getter_ | No docstring. |

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

# Methods within class
Here are methods exposed in the class:
- [\_\_init\_\_](#__init__)
- [append](#append)
- [count\_bytes](#count_bytes)
- [count\_chunks](#count_chunks)
- [count\_records](#count_records)
- [delete](#delete)
- [delete\_all](#delete_all)
- [delete\_many](#delete_many)
- [exists](#exists)
- [extend](#extend)
- [fields](#fields)
- [get](#get)
- [get\_first](#get_first)
- [get\_last](#get_last)
- [info](#info)
- [is\_empty](#is_empty)
- [iterate](#iterate)
- [latest](#latest)
- [load\_field](#load_field)
- [now](#now)
- [now\_dt](#now_dt)
- [open\_blob](#open_blob)
- [position](#position)
- [read\_transaction](#read_transaction)
- [transaction](#transaction)
- [uid](#uid)
- [uids](#uids)
- [write\_transaction](#write_transaction)
- [\_delete\_record](#_delete_record)
- [\_get\_record](#_get_record)
- [\_get\_record\_by\_position](#_get_record_by_position)
- [\_retrieve\_data](#_retrieve_data)
- [\_store\_data](#_store_data)

## \_\_init\_\_
Init

```python
def __init__(self, jinbase):
    ...
```

| Parameter | Description |
| --- | --- |
| jinbase | Jinbase object |

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## append
No docstring

```python
def append(self, value):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## count\_bytes
Count all data bytes in the store.

```python
def count_bytes(self, uid=None):
    ...
```

### Value to return
Returns the count of data bytes

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## count\_chunks
Count all data chunks in the store.

```python
def count_chunks(self, uid=None):
    ...
```

### Value to return
Returns the number of chunks

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## count\_records
Count all records in the store.

```python
def count_records(self):
    ...
```

### Value to return
Returns the number of records

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## delete
No docstring

```python
def delete(self, uid):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## delete\_all
Delete all records in the store

```python
def delete_all(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## delete\_many
No docstring

```python
def delete_many(self, uids):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## exists
No docstring

```python
def exists(self, uid):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## extend
No docstring

```python
def extend(self, values):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## fields
No docstring

```python
def fields(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## get
No docstring

```python
def get(self, uid, default=None):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## get\_first
No docstring

```python
def get_first(self, default=None):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## get\_last
No docstring

```python
def get_last(self, default=None):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## info
No docstring

```python
def info(self, uid):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## is\_empty
Tells whether the store is empty or not

```python
def is_empty(self):
    ...
```

### Value to return
Return a boolean.

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## iterate
No docstring

```python
def iterate(self, *, timespan=None, limit=None, asc=True):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## latest
Retrieve the datetime of the latest write operation.

```python
def latest(self):
    ...
```

### Value to return
Return a datetime string

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## load\_field
No docstring

```python
def load_field(self, uid, field, default=None):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## now
Get the current datetime.

```python
@staticmethod
def now():
    ...
```

### Value to return
Return a datetime string.

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## now\_dt
Get the current datetime.

```python
@staticmethod
def now_dt():
    ...
```

### Value to return
Return a datetime object.

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## open\_blob
No docstring

```python
def open_blob(self, uid):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## position
No docstring

```python
def position(self, uid):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## read\_transaction
Context manager for executing a Read transaction.

```python
def read_transaction(self):
    ...
```

### Value to yield
Yields a `litedbc.Cursor` object

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## transaction
Context manager for executing a transaction.

```python
def transaction(self, transaction_mode=<TransactionMode.DEFERRED: 'DEFERRED'>):
    ...
```

| Parameter | Description |
| --- | --- |
| transaction | Instance of `litedbc.TransactionMode` |

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## uid
No docstring

```python
def uid(self, position):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## uids
No docstring

```python
def uids(self, *, timespan=None, limit=None, asc=True):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## write\_transaction
Context manager for executing a Write transaction.

```python
def write_transaction(self):
    ...
```

### Value to yield
Yields a `litedbc.Cursor` object

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## \_delete\_record
No docstring

```python
def _delete_record(self, record_id):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## \_get\_record
No docstring

```python
def _get_record(self, uid):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## \_get\_record\_by\_position
No docstring

```python
def _get_record_by_position(self, position):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## \_retrieve\_data
No docstring

```python
def _retrieve_data(self, record_id, datatype):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## \_store\_data
No docstring

```python
def _store_data(self, record_id, datatype, value):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>
