###### Jinbase API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | Module | [Source](/src/jinbase/store/depot.py)

# Module Overview
> Module: **jinbase.store.depot**

The Depot store is defined in this module.

## Classes
- [**Depot**](/docs/api/modules/jinbase/store/depot/class-Depot.md): This class represents the Depot store. Note that a Depot object isn't intended to be directly instantiated by the user.
    - [\_abc\_impl](/docs/api/modules/jinbase/store/depot/class-Depot.md#fields-table) = `<_abc._abc_data object at 0x7eb5e3637440>`
    - [chunk\_size](/docs/api/modules/jinbase/store/depot/class-Depot.md#properties-table); _getter_
    - [dbc](/docs/api/modules/jinbase/store/depot/class-Depot.md#properties-table); _getter_
    - [filename](/docs/api/modules/jinbase/store/depot/class-Depot.md#properties-table); _getter_
    - [in\_memory](/docs/api/modules/jinbase/store/depot/class-Depot.md#properties-table); _getter_
    - [is\_closed](/docs/api/modules/jinbase/store/depot/class-Depot.md#properties-table); _getter_
    - [is\_new](/docs/api/modules/jinbase/store/depot/class-Depot.md#properties-table); _getter_
    - [is\_readonly](/docs/api/modules/jinbase/store/depot/class-Depot.md#properties-table); _getter_
    - [jinbase](/docs/api/modules/jinbase/store/depot/class-Depot.md#properties-table); _getter_
    - [model](/docs/api/modules/jinbase/store/depot/class-Depot.md#properties-table); _getter_
    - [timeout](/docs/api/modules/jinbase/store/depot/class-Depot.md#properties-table); _getter_
    - [type\_ref](/docs/api/modules/jinbase/store/depot/class-Depot.md#properties-table); _getter_
    - [append](/docs/api/modules/jinbase/store/depot/class-Depot.md#append): No docstring.
    - [count\_bytes](/docs/api/modules/jinbase/store/depot/class-Depot.md#count_bytes): Count all data bytes in the store.
    - [count\_chunks](/docs/api/modules/jinbase/store/depot/class-Depot.md#count_chunks): Count all data chunks in the store.
    - [count\_records](/docs/api/modules/jinbase/store/depot/class-Depot.md#count_records): Count all records in the store.
    - [delete](/docs/api/modules/jinbase/store/depot/class-Depot.md#delete): No docstring.
    - [delete\_all](/docs/api/modules/jinbase/store/depot/class-Depot.md#delete_all): Delete all records in the store
    - [delete\_many](/docs/api/modules/jinbase/store/depot/class-Depot.md#delete_many): No docstring.
    - [exists](/docs/api/modules/jinbase/store/depot/class-Depot.md#exists): No docstring.
    - [extend](/docs/api/modules/jinbase/store/depot/class-Depot.md#extend): No docstring.
    - [fields](/docs/api/modules/jinbase/store/depot/class-Depot.md#fields): No docstring.
    - [get](/docs/api/modules/jinbase/store/depot/class-Depot.md#get): No docstring.
    - [get\_first](/docs/api/modules/jinbase/store/depot/class-Depot.md#get_first): No docstring.
    - [get\_last](/docs/api/modules/jinbase/store/depot/class-Depot.md#get_last): No docstring.
    - [info](/docs/api/modules/jinbase/store/depot/class-Depot.md#info): No docstring.
    - [is\_empty](/docs/api/modules/jinbase/store/depot/class-Depot.md#is_empty): Tells whether the store is empty or not
    - [iterate](/docs/api/modules/jinbase/store/depot/class-Depot.md#iterate): No docstring.
    - [latest](/docs/api/modules/jinbase/store/depot/class-Depot.md#latest): Retrieve the datetime of the latest write operation.
    - [load\_field](/docs/api/modules/jinbase/store/depot/class-Depot.md#load_field): No docstring.
    - [now](/docs/api/modules/jinbase/store/depot/class-Depot.md#now): Get the current datetime.
    - [now\_dt](/docs/api/modules/jinbase/store/depot/class-Depot.md#now_dt): Get the current datetime.
    - [open\_blob](/docs/api/modules/jinbase/store/depot/class-Depot.md#open_blob): No docstring.
    - [position](/docs/api/modules/jinbase/store/depot/class-Depot.md#position): No docstring.
    - [read\_transaction](/docs/api/modules/jinbase/store/depot/class-Depot.md#read_transaction): Context manager for executing a Read transaction.
    - [transaction](/docs/api/modules/jinbase/store/depot/class-Depot.md#transaction): Context manager for executing a transaction.
    - [uid](/docs/api/modules/jinbase/store/depot/class-Depot.md#uid): No docstring.
    - [uids](/docs/api/modules/jinbase/store/depot/class-Depot.md#uids): No docstring.
    - [write\_transaction](/docs/api/modules/jinbase/store/depot/class-Depot.md#write_transaction): Context manager for executing a Write transaction.
    - [\_delete\_record](/docs/api/modules/jinbase/store/depot/class-Depot.md#_delete_record): No docstring.
    - [\_get\_record](/docs/api/modules/jinbase/store/depot/class-Depot.md#_get_record): No docstring.
    - [\_get\_record\_by\_position](/docs/api/modules/jinbase/store/depot/class-Depot.md#_get_record_by_position): No docstring.
    - [\_retrieve\_data](/docs/api/modules/jinbase/store/depot/class-Depot.md#_retrieve_data): No docstring.
    - [\_store\_data](/docs/api/modules/jinbase/store/depot/class-Depot.md#_store_data): No docstring.

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>
