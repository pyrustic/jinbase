###### Jinbase API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/jinbase/blob/__init__/README.md) | [Source](/src/jinbase/blob/__init__.py)

# Class Blob
> Module: [jinbase.blob.\_\_init\_\_](/docs/api/modules/jinbase/blob/__init__/README.md)
>
> Class: **Blob**
>
> Inheritance: `object`

The Blob class allows a Read access to the blobs of Jinbase records.
This class isn't intended to be directly instantiated by the user.

# Methods within class
Here are methods exposed in the class:
- [\_\_init\_\_](#__init__)
- [close](#close)
- [read](#read)
- [seek](#seek)
- [tell](#tell)
- [write](#write)
- [\_get\_blob\_io\_file](#_get_blob_io_file)
- [\_get\_chunk](#_get_chunk)
- [\_read](#_read)

## \_\_init\_\_
Initialization.

```python
def __init__(self, store, record_id, n_bytes, n_chunks):
    ...
```

| Parameter | Description |
| --- | --- |
| store | Store instance. |
| record\_id | The record's uid. |
| n\_bytes | The size of the blob in bytes. |
| n\_chunks | The number of chunks. |

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## close
Close this Blob instance. Note that this method
is automatically called by the Store's open_blob method.

```python
def close(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## read
Read the blob.

```python
def read(self, length=-1, /):
    ...
```

| Parameter | Description |
| --- | --- |
| length | The number of bytes to read. Defaults to -1 to mean the entire blob. Note that the cursor moves as reads are done. |

### Value to return
Returns bytes or an empty byte.

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## seek
Move the cursor to another position

```python
def seek(self, offset, origin=0, /):
    ...
```

| Parameter | Description |
| --- | --- |
| offset | Offset value |
| origin | os.SEEK_SET, os.SEEK_CUR, or os.SEEK_END. Note that os.SEEK_END referes to position beyond the last character of the file, not the last character itself. |

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## tell
Returns the current position of the cursor

```python
def tell(self):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## write
Jinbase doesn't allow Writes on blobs

```python
def write(self, data, /):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## \_get\_blob\_io\_file
No docstring

```python
def _get_blob_io_file(self, chunk_index):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## \_get\_chunk
No docstring

```python
def _get_chunk(self, blob_slice):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## \_read
No docstring

```python
def _read(self, position, length):
    ...
```

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>
