###### Jinbase API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | Module | [Source](/src/jinbase/store/kv.py)

# Module Overview
> Module: **jinbase.store.kv**

The Kv store is defined in this module.

## Classes
- [**Kv**](/docs/api/modules/jinbase/store/kv/class-Kv.md): This class represents the Kv store. Note that a Kv object isn't intended to be directly instantiated by the user.
    - [\_abc\_impl](/docs/api/modules/jinbase/store/kv/class-Kv.md#fields-table) = `<_abc._abc_data object at 0x789010e45800>`
    - [chunk\_size](/docs/api/modules/jinbase/store/kv/class-Kv.md#properties-table); _getter_
    - [dbc](/docs/api/modules/jinbase/store/kv/class-Kv.md#properties-table); _getter_
    - [filename](/docs/api/modules/jinbase/store/kv/class-Kv.md#properties-table); _getter_
    - [in\_memory](/docs/api/modules/jinbase/store/kv/class-Kv.md#properties-table); _getter_
    - [is\_closed](/docs/api/modules/jinbase/store/kv/class-Kv.md#properties-table); _getter_
    - [is\_new](/docs/api/modules/jinbase/store/kv/class-Kv.md#properties-table); _getter_
    - [is\_readonly](/docs/api/modules/jinbase/store/kv/class-Kv.md#properties-table); _getter_
    - [jinbase](/docs/api/modules/jinbase/store/kv/class-Kv.md#properties-table); _getter_
    - [model](/docs/api/modules/jinbase/store/kv/class-Kv.md#properties-table); _getter_
    - [timeout](/docs/api/modules/jinbase/store/kv/class-Kv.md#properties-table); _getter_
    - [type\_ref](/docs/api/modules/jinbase/store/kv/class-Kv.md#properties-table); _getter_
    - [count\_bytes](/docs/api/modules/jinbase/store/kv/class-Kv.md#count_bytes): Count all data bytes in the store.
    - [count\_chunks](/docs/api/modules/jinbase/store/kv/class-Kv.md#count_chunks): Count all data chunks in the store.
    - [count\_records](/docs/api/modules/jinbase/store/kv/class-Kv.md#count_records): Count all records in the store.
    - [delete](/docs/api/modules/jinbase/store/kv/class-Kv.md#delete): No docstring.
    - [delete\_all](/docs/api/modules/jinbase/store/kv/class-Kv.md#delete_all): Delete all records in the store
    - [delete\_many](/docs/api/modules/jinbase/store/kv/class-Kv.md#delete_many): No docstring.
    - [exists](/docs/api/modules/jinbase/store/kv/class-Kv.md#exists): No docstring.
    - [fields](/docs/api/modules/jinbase/store/kv/class-Kv.md#fields): No docstring.
    - [get](/docs/api/modules/jinbase/store/kv/class-Kv.md#get): No docstring.
    - [info](/docs/api/modules/jinbase/store/kv/class-Kv.md#info): No docstring.
    - [int\_keys](/docs/api/modules/jinbase/store/kv/class-Kv.md#int_keys): No docstring.
    - [is\_empty](/docs/api/modules/jinbase/store/kv/class-Kv.md#is_empty): Tells whether the store is empty or not
    - [iterate](/docs/api/modules/jinbase/store/kv/class-Kv.md#iterate): No docstring.
    - [key](/docs/api/modules/jinbase/store/kv/class-Kv.md#key): No docstring.
    - [keys](/docs/api/modules/jinbase/store/kv/class-Kv.md#keys): No docstring.
    - [latest](/docs/api/modules/jinbase/store/kv/class-Kv.md#latest): Retrieve the datetime of the latest write operation.
    - [load\_field](/docs/api/modules/jinbase/store/kv/class-Kv.md#load_field): No docstring.
    - [now](/docs/api/modules/jinbase/store/kv/class-Kv.md#now): Get the current datetime.
    - [now\_dt](/docs/api/modules/jinbase/store/kv/class-Kv.md#now_dt): Get the current datetime.
    - [open\_blob](/docs/api/modules/jinbase/store/kv/class-Kv.md#open_blob): No docstring.
    - [read\_transaction](/docs/api/modules/jinbase/store/kv/class-Kv.md#read_transaction): Context manager for executing a Read transaction.
    - [replace](/docs/api/modules/jinbase/store/kv/class-Kv.md#replace): No docstring.
    - [set](/docs/api/modules/jinbase/store/kv/class-Kv.md#set): No docstring.
    - [str\_keys](/docs/api/modules/jinbase/store/kv/class-Kv.md#str_keys): No docstring.
    - [transaction](/docs/api/modules/jinbase/store/kv/class-Kv.md#transaction): Context manager for executing a transaction.
    - [uid](/docs/api/modules/jinbase/store/kv/class-Kv.md#uid): No docstring.
    - [update](/docs/api/modules/jinbase/store/kv/class-Kv.md#update): data is a dictionary
    - [write\_transaction](/docs/api/modules/jinbase/store/kv/class-Kv.md#write_transaction): Context manager for executing a Write transaction.
    - [\_delete\_record](/docs/api/modules/jinbase/store/kv/class-Kv.md#_delete_record): No docstring.
    - [\_get\_record\_by\_key](/docs/api/modules/jinbase/store/kv/class-Kv.md#_get_record_by_key): No docstring.
    - [\_retrieve\_data](/docs/api/modules/jinbase/store/kv/class-Kv.md#_retrieve_data): No docstring.
    - [\_store\_data](/docs/api/modules/jinbase/store/kv/class-Kv.md#_store_data): No docstring.

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>
