[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI package version](https://img.shields.io/pypi/v/jinbase)](https://pypi.org/project/jinbase)
[![Downloads](https://static.pepy.tech/badge/jinbase)](https://pepy.tech/project/jinbase)


<!-- Cover -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/assets/jinbase/cover.jpg" alt="Cover image" width="800">
    <p align="center">
        <a href="https://commons.wikimedia.org/wiki/File:Rudolf_Reschreiter_Blick_von_der_H%C3%B6llentalangerh%C3%BCtte_zum_H%C3%B6llentalgletscher_und_den_Riffelwandspitzen_1921.jpg">Rudolf Reschreiter</a>, Public domain, via Wikimedia Commons
    </p>
</div>

<!-- Intro Text -->
# Jinbase
<b>Multi-model transactional embedded database</b>


## Table of contents
- [Overview](#overview)
    - [Multiple data models coexisting in a single embedded database](#multiple-data-models-coexisting-in-a-single-embedded-database)
    - [Support for transactions and complex data of arbitrary size](#support-for-transactions-and-complex-data-of-arbitrary-size)
    - [Bulk and partial access to records from byte-level to field-level](#bulk-and-partial-access-to-records-from-byte-level-to-field-level)
    - [Highly configurable database and timestamped records](#highly-configurable-database-and-timestamped-records)
- [Why use Jinbase ?](#why-use-jinbase-)
- [Data models and their corresponding storage interfaces](#data-models-and-their-corresponding-storage-interfaces)
    - [Kv](#kv)
    - [Depot](#depot)
    - [Queue](#queue)
    - [Stack](#stack)
    - [Relational](#relational)
- [The unified BLOB interface](#the-unified-blob-interface)
- [Command line interface](#command-line-interface)
- [Related projects](#related-projects)
- [Testing and contributing](#testing-and-contributing)
- [Installation](#installation)


# Overview
**Jinbase** (pronounced as **/ˈdʒɪnˌbeɪs/**) is a multi-model [transactional](https://en.wikipedia.org/wiki/Database_transaction) [embedded database](https://en.wikipedia.org/wiki/Embedded_database) that uses [SQLite](https://www.sqlite.org/) as storage engine. Its reference implementation is an eponymous lightweight [Python](https://www.python.org/) library available on [PyPI](#installation).


## Multiple data models coexisting in a single embedded database
A single Jinbase database supports **key-value**, **depot**, **queue**, **stack**, and **relational** data models. While a Jinbase file can be populated with multi-model data, depending on the needs, it is quite possible to dedicate a database file to a given model.

For each of the first four data models, there is a programmatic interface accessible via an eponymous property of a Jinbase instance.

## Support for transactions and complex data of arbitrary size
Having SQLite as the storage engine allows Jinbase to benefit from [transactions](https://www.sqlite.org/lang_transaction.html). Jinbase ensures that at the top level, reads and writes on key-value, depot, queue and stack stores are transactional. For user convenience, context managers are exposed to create transactions of different modes.

When for a write operation, the user submits data, whether it is a dictionary, string or integer, Jinbase serializes (except binary data), chunks and stores the data iteratively with the [Paradict](https://github.com/pyrustic/paradict) compact binary data format. This then allows for the smooth storage of complex data of [arbitrary size](https://www.sqlite.org/limits.html) with Jinbase.

## Bulk and partial access to records from byte-level to field-level
Jinbase not only offers bulk access to records, but also two levels of partial access granularity.

SQLite has an impressive capability which is [incremental I/O](https://sqlite.org/c3ref/blob_open.html) for [BLOBs](https://www.sqlite.org/datatype3.html). While this capability is designed to target an individual BLOB column in a row, Jinbase extends this so that for each record, incremental reads cover all chunks as if they were a single [unified BLOB](#the-unified-blob-interface).

For [dictionary](https://en.wikipedia.org/wiki/Associative_array) records only, Jinbase automatically creates and maintains a lightweight index consisting of pointers to root fields, which then allows extracting from an arbitrary record the contents of a field automatically deserialized before being returned.

## Highly configurable database and timestamped records
Jinbase exposes a database connection object to the underlying SQLite storage engine, allowing for sophisticated configuration. The [Paradict](https://github.com/pyrustic/paradict) binary data format used for serializing records also allows for customizing data types via a `paradict.TypeRef` object.

Each record stored in a key-value, depot, queue, or stack store is automatically timestamped. This allows the user to provide a `time_range` tuple when querying records. The precision of the timestamp, which defaults to milliseconds, can also be configured.



# Why use Jinbase ?
Jinbase implements persistence for familiar data models whose stores coexist in a single file with an intuitive programmatic interface. Supported [data types](https://github.com/pyrustic/paradict) range from simple to complex and of [arbitrary size](https://www.sqlite.org/limits.html).

For convenience, all Jinbase-related tables are prefixed with `jinbase_`, allowing the user to define their own tables and interact with them as they would with a regular SQLite database. 

Thanks to its multi-model coexistence capability, Jinbase can be used to open legacy SQLite databases to add four useful data models (key-value, depot, queue, and stack).

All this makes Jinbase relevant from prototype to production stages of software development of various sizes and scopes. 

Following are few of the most obvious use cases:

- Storing user preferences
- Persisting session data before exit
- Order-based processing of data streams
- Exposing data for other processes
- Upgrading legacy SQLite files with new data models
- Bespoke data persistence solution

# Data models and their corresponding storage interfaces
Following subsections discuss data models and their corresponding storage interfaces.

## Kv
The [key-value](https://en.wikipedia.org/wiki/Key%E2%80%93value_database) data model associates to a string or an integer key, a value that is serializable with the [Paradict](https://github.com/pyrustic/paradict) binary data format. 

String keys can be searched with a [glob](https://en.wikipedia.org/wiki/Glob_(programming)) pattern and integer keys can be searched within a range of numbers. Since records are automatically timestamped, a `time_range` tuple can be provided by the user to search for them as well as keys.

Example:

```python
import os.path
from datetime import datetime
from jinbase import Jinbase, JINBASE_HOME

user_data = {"id": 42, "name": "alex", "created_at": datetime.now(),
             "photo": b'\x45\xA6\x42\xDF\x69',
             "books": {"sci-fi": ["book 1", "book 2"],
                       "thriller": ["book 3", ["book4"]]}}

db_filename = os.path.join(JINBASE_HOME, "test.db")

with Jinbase(db_filename) as db:
  # set 'user'
  kv_store = db.kv
  kv_store.set("user", user_data)  # returns a UID

  # get 'user'
  data = kv_store.get("user")
  assert data == user_data

  # count total records and bytes
  print(kv_store.count_records())
  print(kv_store.count_bytes("user"))

  # list keys (the time_range is optional)
  time_range = ("2024-11-20 10:00:00Z", "2035-11-20 10:00:00Z")
  print(tuple(kv_store.keys(time_range=time_range)))

  # find string keys with a glob pattern
  print(tuple(kv_store.str_keys(glob="use*")))

  # load the 'books' field (partial access)
  books = kv_store.load_field("user", "books")
  assert books == user_data["books"]

  # iterate (descending order)
  for key, value in kv_store.iterate(asc=False):
    pass
```
> Check out the API reference for the [key-value store](https://github.com/pyrustic/jinbase/blob/master/docs/api/modules/jinbase/store/kv/class-Kv.md).


## Depot
The depot data model shares similarities with the [List](https://en.wikipedia.org/wiki/List_(abstract_data_type)) data structure. An
unique identifier (UID) is automatically assigned to a record appended to the store. This record can be retrieved later either by its unique identifier or by its [0-based](https://en.wikipedia.org/wiki/Zero-based_numbering) position in the store.

Example:

```python
import os.path
from datetime import datetime
from jinbase import Jinbase, JINBASE_HOME

user_data = {"id": 42, "name": "alex", "created_at": datetime.now(),
             "photo": b'\x45\xA6\x42\xDF\x69',
             "books": {"sci-fi": ["book 1", "book 2"],
                       "thriller": ["book 3", ["book4"]]}}

db_filename = os.path.join(JINBASE_HOME, "test.db")

with Jinbase(db_filename) as db:
    # append 'user_data' to the depot
    depot_store = db.depot
    uid = depot_store.append(user_data)

    # get 'user_data'
    data = depot_store.get(uid)
    assert data == user_data

    # get the record at position 0 in the depot
    print(depot_store.uid(0))  # prints the UID
    # get the position of a record in the depot
    print(depot_store.position(uid))  # prints the position

    # count total records and bytes
    print(depot_store.count_records())
    print(depot_store.count_bytes(uid))

    # list UIDs (unique identifiers)
    time_range = ("2024-11-20 10:00:00Z", "2035-11-20 10:00:00Z")
    print(tuple(depot_store.uids(time_range=time_range)))

    # load the 'books' field (partial access)
    books = depot_store.load_field(uid, "books")
    assert books == user_data["books"]

    # iterate (descending order)
    for uid, data in depot_store.iterate(asc=False):
        pass
```

> Check out the API reference for the [depot store](https://github.com/pyrustic/jinbase/blob/master/docs/api/modules/jinbase/store/depot/class-Depot.md).

## Queue
The [queue](https://en.wikipedia.org/wiki/Queue_(abstract_data_type)) data model like other stores, is transactional. While this store provides methods to enqueue and dequeue records, there is also `peek_xxx` methods to look at the record at the front or the back of the queue, that is, read it without dequeuing.

Example:
 
```python
import os.path
from datetime import datetime
from jinbase import Jinbase, JINBASE_HOME

user_data = {"id": 42, "name": "alex", "created_at": datetime.now(),
             "photo": b'\x45\xA6\x42\xDF\x69',
             "books": {"sci-fi": ["book 1", "book 2"],
                       "thriller": ["book 3", ["book4"]]}}

db_filename = os.path.join(JINBASE_HOME, "test.db")

with Jinbase(db_filename) as db:
    # enqueue 'user_data'
    queue_store = db.queue
    queue_store.enqueue(user_data)  # returns a UID

    # peek
    data1 = queue_store.peek_front()
    data2 = queue_store.peek_back()
    assert data1 == data2 == user_data

    # dequeue
    data = queue_store.dequeue()
    assert data == user_data

    # we could have dequeued the record inside a transaction
    # to ensure that its processing completed successfully
    # (if it fails, an automatic rollback is performed)
    with db.write_transaction():
        data = queue_store.dequeue()
        # from here, process the data
        ...
```

> Check out the API reference for the [queue store](https://github.com/pyrustic/jinbase/blob/master/docs/api/modules/jinbase/store/queue/class-Queue.md).

## Stack
The [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) data model like other stores, is transactional. While this store provides methods to push and pop records, there is also a `peek` method to look at the record on top of the stack, that is, read it without popping it from the stack.

```python
import os.path
from datetime import datetime
from jinbase import Jinbase, JINBASE_HOME

user_data = {"id": 42, "name": "alex", "created_at": datetime.now(),
             "photo": b'\x45\xA6\x42\xDF\x69',
             "books": {"sci-fi": ["book 1", "book 2"],
                       "thriller": ["book 3", ["book4"]]}}

db_filename = os.path.join(JINBASE_HOME, "test.db")

with Jinbase(db_filename) as db:
    # push 'user_data' on top of the stack
    stack_store = db.stack
    stack_store.push(user_data)

    # peek
    data = stack_store.peek()
    assert data == user_data

    # pop 'user_data'
    data = stack_store.pop()
    assert data == user_data

    # we could have popped the record inside a transaction
    # to ensure that its processing completed successfully
    # (if it fails, an automatic rollback is performed)
    with db.write_transaction():
        data = stack_store.pop()
        # from here, process the data
        ...
```

> Check out the API reference for the [stack store](https://github.com/pyrustic/jinbase/blob/master/docs/api/modules/jinbase/store/stack/class-Stack.md).

## Relational
As Jinbase uses [SQLite](https://en.wikipedia.org/wiki/SQLite) as its storage engine, it de facto supports the [relational](https://en.wikipedia.org/wiki/Relational_model) data model for which it exposes an interface, [LiteDBC](https://github.com/pyrustic/litedbc), for querying SQLite.

LiteDBC is an SQL interface compliant with the DB-API 2.0 specification described by [PEP 249](https://peps.python.org/pep-0249/), itself wrapping Python's [sqlite3](https://docs.python.org/3/library/sqlite3.html) module for a more intuitive interface and multithreading support by default.

Example:

```python
import os.path
from jinbase import Jinbase, JINBASE_HOME

db_filename = os.path.join(JINBASE_HOME, "test.db")

with Jinbase(db_filename) as db:
    lite_dbc = db.dbc
    with lite_dbc.transaction() as cursor:
        # query the table names that exist in this database
        query = ("SELECT name FROM sqlite_master "
                 "WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        cursor.execute(query)
        # Although the Cursor object already has the traditional "fetchone",
        # "fetchmany" and "fetchall" methods, LiteDBC adds a new lazy "fetch"
        # method for intuitive iteration.
        # Note that 'fetch()' accepts 'limit' and 'buffer_size' as arguments.
        for row in cursor.fetch():
            table_name = row[0]
            print(table_name)

```

> Check out [LiteDBC](https://github.com/pyrustic/litedbc).

# The unified BLOB interface
When for a write operation, the user submits data, whether it is a dictionary, string or integer, Jinbase serializes (except binary data), chunks and stores the data iteratively with the [Paradict](https://github.com/pyrustic/paradict) compact binary data format. Under the hood, these chunks are actually stored as SQLite Binary Large Objects ([BLOBs](https://www.sqlite.org/datatype3.html)). 

SQLite has an impressive capability which is [incremental I/O](https://sqlite.org/c3ref/blob_open.html) for BLOBs. While this capability is designed to target an individual BLOB column in a row, Jinbase extends it to enable incremental reads of record chunks as if they form a single [unified BLOB](#the-unified-blob-interface).

Example:

```python
import os.path
from jinbase import Jinbase, JINBASE_HOME

db_filename = os.path.join(JINBASE_HOME, "test.db")
CHUNK_SIZE = 1  # 1 byte, thus a 5-byte input will have 5 chunks

# The 'chunk_size' can be defined only once when Jinbase creates or opens
# the database for first time. New values for 'chunk_size' will be ignored.
# So, for this example to work, ensure that the 'db_filename' is nonexistent.
with Jinbase(db_filename, chunk_size=CHUNK_SIZE) as db:
    # some binary data
    USER_DATA = b'\x20\x55\xA9\xBC\x69\x42\xD1'  # seven bytes !
    # set the data
    kv_store = db.kv
    kv_store.set("user", USER_DATA)
    # count chunks
    n_chunks = kv_store.count_chunks("user")
    assert n_chunks == len(USER_DATA)  # seven bytes !

    # access the unified blob interface for incremental reads
    with kv_store.open_blob("user") as blob:
        # read the entire unified blob
        data = blob.read()
        assert data == USER_DATA
        assert blob.tell() == len(USER_DATA)  # cursor position
        assert blob.read() == b''
        # move the cursor back to the beginning of the blob
        blob.seek(0)
        # read the first byte
        assert blob.read(1) == bytes([USER_DATA[0]]) 
        # read the last byte
        assert blob[-1] == bytes([USER_DATA[-1]])
        # read a slice
        slice_obj = slice(2, 5)
        assert blob[slice_obj] == USER_DATA[slice_obj]
```

> The unified BLOB interface for incremental reads will only work on Python >=3.11

# Command line interface
Not yet implemented.

# Related projects
- [LiteDBC](https://github.com/pyrustic/litedbc): Lite database connector
- [Paradict](https://github.com/pyrustic/paradict): Streamable multi-format serialization with schema 
- [Asyncpal](https://github.com/pyrustic/asyncpal): Preemptive concurrency and parallelism for sporadic workloads 
- [KvF](https://github.com/pyrustic/kvf): The key-value file format with sections 

# Testing and contributing
Feel free to **open an issue** to report a bug, suggest some changes, show some useful code snippets, or discuss anything related to this project. You can also directly email [me](https://pyrustic.github.io/#contact).

## Setup your development environment
Following are instructions to setup your development environment

```bash
# create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# clone the project then change into its directory
git clone https://github.com/pyrustic/jinbase.git
cd jinbase

# install the package locally (editable mode)
pip install -e .

# run tests
python -m tests

# deactivate the virtual environment
deactivate
```

<p align="right"><a href="#readme">Back to top</a></p>

# Installation
**Jinbase** is **cross-platform**. It is built on [Ubuntu](https://ubuntu.com/download/desktop) and should work on **Python 3.8** or **newer**.

## Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

## Install for the first time

```bash
pip install jinbase
```

## Upgrade the package
```bash
pip install jinbase --upgrade --upgrade-strategy eager
```

## Deactivate the virtual environment
```bash
deactivate
```

<p align="right"><a href="#readme">Back to top</a></p>

# About the author
Hello world, I'm Alex (😎️), a tech enthusiast and the architect of [Pyrustic](https://pyrustic.github.io) ! Feel free to get in touch with [me](https://pyrustic.github.io/#contact) !

<br>
<br>
<br>

[Back to top](#readme)
