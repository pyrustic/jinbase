###### Jinbase API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | Module | [Source](/src/jinbase/store/__init__.py)

# Module Overview
> Module: **jinbase.store.\_\_init\_\_**

The abstract Store class is defined in this module.

## Classes
- [**RecordInfo**](/docs/api/modules/jinbase/store/__init__/class-RecordInfo.md): Named tuple returned by store.info()
    - uid: Alias for field number 0
    - datatype: Alias for field number 1
    - created\_at: Alias for field number 2
- [**Store**](/docs/api/modules/jinbase/store/__init__/class-Store.md): Abstract Store class intended to be subclassed by the Kv, Depot, Queue, and Stack stores
    - [\_abc\_impl](/docs/api/modules/jinbase/store/__init__/class-Store.md#fields-table) = `<_abc._abc_data object at 0x7eb5e3670540>`
    - [chunk\_size](/docs/api/modules/jinbase/store/__init__/class-Store.md#properties-table); _getter_
    - [dbc](/docs/api/modules/jinbase/store/__init__/class-Store.md#properties-table); _getter_
    - [filename](/docs/api/modules/jinbase/store/__init__/class-Store.md#properties-table); _getter_
    - [in\_memory](/docs/api/modules/jinbase/store/__init__/class-Store.md#properties-table); _getter_
    - [is\_closed](/docs/api/modules/jinbase/store/__init__/class-Store.md#properties-table); _getter_
    - [is\_new](/docs/api/modules/jinbase/store/__init__/class-Store.md#properties-table); _getter_
    - [is\_readonly](/docs/api/modules/jinbase/store/__init__/class-Store.md#properties-table); _getter_
    - [jinbase](/docs/api/modules/jinbase/store/__init__/class-Store.md#properties-table); _getter_
    - [model](/docs/api/modules/jinbase/store/__init__/class-Store.md#properties-table); _getter_
    - [timeout](/docs/api/modules/jinbase/store/__init__/class-Store.md#properties-table); _getter_
    - [type\_ref](/docs/api/modules/jinbase/store/__init__/class-Store.md#properties-table); _getter_
    - [count\_bytes](/docs/api/modules/jinbase/store/__init__/class-Store.md#count_bytes): Count all data bytes in the store.
    - [count\_chunks](/docs/api/modules/jinbase/store/__init__/class-Store.md#count_chunks): Count all data chunks in the store.
    - [count\_records](/docs/api/modules/jinbase/store/__init__/class-Store.md#count_records): Count all records in the store.
    - [delete\_all](/docs/api/modules/jinbase/store/__init__/class-Store.md#delete_all): Delete all records in the store
    - [is\_empty](/docs/api/modules/jinbase/store/__init__/class-Store.md#is_empty): Tells whether the store is empty or not
    - [latest](/docs/api/modules/jinbase/store/__init__/class-Store.md#latest): Retrieve the datetime of the latest write operation.
    - [now](/docs/api/modules/jinbase/store/__init__/class-Store.md#now): Get the current datetime.
    - [now\_dt](/docs/api/modules/jinbase/store/__init__/class-Store.md#now_dt): Get the current datetime.
    - [read\_transaction](/docs/api/modules/jinbase/store/__init__/class-Store.md#read_transaction): Context manager for executing a Read transaction.
    - [transaction](/docs/api/modules/jinbase/store/__init__/class-Store.md#transaction): Context manager for executing a transaction.
    - [write\_transaction](/docs/api/modules/jinbase/store/__init__/class-Store.md#write_transaction): Context manager for executing a Write transaction.
    - [\_delete\_record](/docs/api/modules/jinbase/store/__init__/class-Store.md#_delete_record): No docstring.
    - [\_retrieve\_data](/docs/api/modules/jinbase/store/__init__/class-Store.md#_retrieve_data): No docstring.
    - [\_store\_data](/docs/api/modules/jinbase/store/__init__/class-Store.md#_store_data): No docstring.

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>
