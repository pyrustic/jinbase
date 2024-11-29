###### Jinbase API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/jinbase/store/queue/README.md) | [Source](/src/jinbase/store/queue.py)

# Class Queue
> Module: [jinbase.store.queue](/docs/api/modules/jinbase/store/queue/README.md)
>
> Class: **Queue**
>
> Inheritance: [jinbase.store.Store](/docs/api/modules/jinbase/store/class-Store.md)

This class represents the Queue store.
Note that a Queue object isn't intended to be directly
instantiated by the user.

## Fields table
Here are fields exposed in the class:

| Field | Value |
| --- | --- |
| \_abc\_impl | `<_abc._abc_data object at 0x789010e46240>` |

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
- [back\_uid](#back_uid)
- [count\_back\_bytes](#count_back_bytes)
- [count\_back\_chunks](#count_back_chunks)
- [count\_bytes](#count_bytes)
- [count\_chunks](#count_chunks)
- [count\_front\_bytes](#count_front_bytes)
- [count\_front\_chunks](#count_front_chunks)
- [count\_records](#count_records)
- [delete\_all](#delete_all)
- [dequeue](#dequeue)
- [enqueue](#enqueue)
- [enqueue\_many](#enqueue_many)
- [front\_uid](#front_uid)
- [info\_back](#info_back)
- [info\_front](#info_front)
- [is\_empty](#is_empty)
- [latest](#latest)
- [now](#now)
- [now\_dt](#now_dt)
- [peek\_back](#peek_back)
- [peek\_front](#peek_front)
- [read\_transaction](#read_transaction)
- [transaction](#transaction)
- [write\_transaction](#write_transaction)
- [\_delete\_record](#_delete_record)
- [\_get\_back](#_get_back)
- [\_get\_front](#_get_front)
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

## back\_uid
No docstring

```python
def back_uid(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## count\_back\_bytes
No docstring

```python
def count_back_bytes(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## count\_back\_chunks
No docstring

```python
def count_back_chunks(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## count\_bytes
Count all data bytes in the store.

```python
def count_bytes(self):
    ...
```

### Value to return
Returns the count of data bytes

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## count\_chunks
Count all data chunks in the store.

```python
def count_chunks(self):
    ...
```

### Value to return
Returns the number of chunks

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## count\_front\_bytes
No docstring

```python
def count_front_bytes(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## count\_front\_chunks
No docstring

```python
def count_front_chunks(self):
    ...
```

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

## delete\_all
Delete all records in the store

```python
def delete_all(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## dequeue
No docstring

```python
def dequeue(self, default=None):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## enqueue
No docstring

```python
def enqueue(self, value):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## enqueue\_many
No docstring

```python
def enqueue_many(self, values):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## front\_uid
No docstring

```python
def front_uid(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## info\_back
No docstring

```python
def info_back(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## info\_front
No docstring

```python
def info_front(self):
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

## latest
Retrieve the datetime of the latest write operation.

```python
def latest(self):
    ...
```

### Value to return
Return a datetime string

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

## peek\_back
No docstring

```python
def peek_back(self, default=None):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## peek\_front
No docstring

```python
def peek_front(self, default=None):
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

## \_get\_back
No docstring

```python
def _get_back(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## \_get\_front
No docstring

```python
def _get_front(self):
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
