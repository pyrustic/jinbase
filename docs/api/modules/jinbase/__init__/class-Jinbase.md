###### Jinbase API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/jinbase/__init__/README.md) | [Source](/src/jinbase/__init__.py)

# Class Jinbase
> Module: [jinbase.\_\_init\_\_](/docs/api/modules/jinbase/__init__/README.md)
>
> Class: **Jinbase**
>
> Inheritance: `object`

The Jinbase class. A Jinbase object is intended to
be directly instantiated by the user.

## Properties table
Here are properties exposed in the class:

| Property | Methods | Description |
| --- | --- | --- |
| chunk\_size | _getter_ | No docstring. |
| created\_at | _getter_ | No docstring. |
| creation\_dt | _getter_ | No docstring. |
| dbc | _getter_ | The instance of litedbc.LiteDBC |
| depot | _getter_ | No docstring. |
| filename | _getter_ | No docstring. |
| in\_memory | _getter_ | No docstring. |
| is\_closed | _getter_ | No docstring. |
| is\_destroyed | _getter_ | No docstring. |
| is\_new | _getter_ | No docstring. |
| is\_readonly | _getter_ | No docstring. |
| kv | _getter_ | No docstring. |
| queue | _getter_ | No docstring. |
| stack | _getter_ | No docstring. |
| timeout | _getter_ | No docstring. |
| timestamp\_precision | _getter_ | No docstring. |
| type\_ref | _getter_ | No docstring. |
| version | _getter_ | No docstring. |

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

# Methods within class
Here are methods exposed in the class:
- [\_\_init\_\_](#__init__)
- [backup](#backup)
- [close](#close)
- [copy](#copy)
- [count\_bytes](#count_bytes)
- [count\_chunks](#count_chunks)
- [count\_records](#count_records)
- [destroy](#destroy)
- [get\_journal\_mode](#get_journal_mode)
- [get\_locking\_mode](#get_locking_mode)
- [get\_sync\_mode](#get_sync_mode)
- [interrupt](#interrupt)
- [iterdump](#iterdump)
- [latest](#latest)
- [now](#now)
- [now\_dt](#now_dt)
- [read\_transaction](#read_transaction)
- [scan](#scan)
- [set\_journal\_mode](#set_journal_mode)
- [set\_locking\_mode](#set_locking_mode)
- [set\_progress\_handler](#set_progress_handler)
- [set\_sync\_mode](#set_sync_mode)
- [set\_trace\_callback](#set_trace_callback)
- [transaction](#transaction)
- [vacuum](#vacuum)
- [vacuum\_into](#vacuum_into)
- [write\_transaction](#write_transaction)

## \_\_init\_\_
Init.

```python
def __init__(self, filename=None, *, auto_create=True, is_readonly=False, timeout=5.0, type_ref=None, chunk_size=1048576, timestamp_precision=<TimestampPrecision.MILLISECONDS: 3>):
    ...
```

| Parameter | Description |
| --- | --- |
| filename | The filename of the Jinbase database. If the pointed file doesn't exist, it will be created if `auto_create` is set to True. |
| auto\_create | Boolean to tell whether a nonexistent database file should automatically be created or not. Defaults to True. |
| is\_readonly | Boolean to tell whether the database connection should be in readonly or not. |
| timeout | Timeout in seconds for all database operations. Defaults to the value of `jinbase.TIMEOUT` |
| type\_ref | A paradict.TypeRef instance |
| chunk\_size | Chunk size in bytes. Defaults to `jinbase.CHUNK_SIZE`. Note that this value is only relevant when the Jinbase tables are created. |
| timestamp\_precision | An instance of the `jinbase.TimestampPrecision` namedtuple. Defaults to `jinbase.TIMESTAMP_PRECISION`. Note that this value is only relevant when the Jinbase tables are created. |

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## backup
No docstring

```python
def backup(self, dst, *, pages=-1, progress=None, sleep=0.25):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## close
Close the connection

```python
def close(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## copy
Create a new Jinbase instance that
points to the same database file

```python
def copy(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## count\_bytes
No docstring

```python
def count_bytes(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## count\_chunks
No docstring

```python
def count_chunks(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## count\_records
No docstring

```python
def count_records(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## destroy
Destroy the database file

```python
def destroy(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## get\_journal\_mode
No docstring

```python
def get_journal_mode(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## get\_locking\_mode
No docstring

```python
def get_locking_mode(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## get\_sync\_mode
No docstring

```python
def get_sync_mode(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## interrupt
No docstring

```python
def interrupt(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## iterdump
Returns an iterator to the dump of the database
in an SQL text format

```python
def iterdump(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## latest
Get the utc datetime of the latest operation.

```python
def latest(self):
    ...
```

### Value to return
A utc instance of `datetime.datetime`

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## now
Get the current utc datetime.

```python
@staticmethod
def now():
    ...
```

### Value to return
A utc instance of `datetime.datetime`

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## now\_dt
Get the current utc datetime.

```python
@staticmethod
def now_dt():
    ...
```

### Value to return
A utc string

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## read\_transaction
No docstring

```python
def read_transaction(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## scan
Scan the Jinbase database

```python
def scan(self):
    ...
```

### Value to return
A dictionary object whose keys are jinbase.Model namedtuples
and values are tuples of the total record count and total byte count.

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## set\_journal\_mode
No docstring

```python
def set_journal_mode(self, journal_mode):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## set\_locking\_mode
No docstring

```python
def set_locking_mode(self, locking_mode):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## set\_progress\_handler
No docstring

```python
def set_progress_handler(self, callback, n):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## set\_sync\_mode
No docstring

```python
def set_sync_mode(self, sync_mode):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## set\_trace\_callback
No docstring

```python
def set_trace_callback(self, callback):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## transaction
No docstring

```python
def transaction(self, transaction_mode=<TransactionMode.DEFERRED: 'DEFERRED'>):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## vacuum
Vacuum the database

```python
def vacuum(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## vacuum\_into
Vacuum into a file whose name is provided via `dst`.

```python
def vacuum_into(self, dst):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## write\_transaction
No docstring

```python
def write_transaction(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>
