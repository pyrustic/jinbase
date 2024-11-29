###### Jinbase API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | Module | [Source](/src/jinbase/store/stack.py)

# Module Overview
> Module: **jinbase.store.stack**

The Stack store is defined in this module.

## Classes
- [**Stack**](/docs/api/modules/jinbase/store/stack/class-Stack.md): This class represents the Stack store. Note that a Stack object isn't intended to be directly instantiated by the user.
    - [\_abc\_impl](/docs/api/modules/jinbase/store/stack/class-Stack.md#fields-table) = `<_abc._abc_data object at 0x7588e47c6740>`
    - [chunk\_size](/docs/api/modules/jinbase/store/stack/class-Stack.md#properties-table); _getter_
    - [dbc](/docs/api/modules/jinbase/store/stack/class-Stack.md#properties-table); _getter_
    - [filename](/docs/api/modules/jinbase/store/stack/class-Stack.md#properties-table); _getter_
    - [in\_memory](/docs/api/modules/jinbase/store/stack/class-Stack.md#properties-table); _getter_
    - [is\_closed](/docs/api/modules/jinbase/store/stack/class-Stack.md#properties-table); _getter_
    - [is\_new](/docs/api/modules/jinbase/store/stack/class-Stack.md#properties-table); _getter_
    - [is\_readonly](/docs/api/modules/jinbase/store/stack/class-Stack.md#properties-table); _getter_
    - [jinbase](/docs/api/modules/jinbase/store/stack/class-Stack.md#properties-table); _getter_
    - [model](/docs/api/modules/jinbase/store/stack/class-Stack.md#properties-table); _getter_
    - [timeout](/docs/api/modules/jinbase/store/stack/class-Stack.md#properties-table); _getter_
    - [type\_ref](/docs/api/modules/jinbase/store/stack/class-Stack.md#properties-table); _getter_
    - [count\_bytes](/docs/api/modules/jinbase/store/stack/class-Stack.md#count_bytes): Count all data bytes in the store.
    - [count\_chunks](/docs/api/modules/jinbase/store/stack/class-Stack.md#count_chunks): Count all data chunks in the store.
    - [count\_records](/docs/api/modules/jinbase/store/stack/class-Stack.md#count_records): Count all records in the store.
    - [count\_top\_bytes](/docs/api/modules/jinbase/store/stack/class-Stack.md#count_top_bytes): No docstring.
    - [count\_top\_chunks](/docs/api/modules/jinbase/store/stack/class-Stack.md#count_top_chunks): No docstring.
    - [delete\_all](/docs/api/modules/jinbase/store/stack/class-Stack.md#delete_all): Delete all records in the store
    - [info\_top](/docs/api/modules/jinbase/store/stack/class-Stack.md#info_top): No docstring.
    - [is\_empty](/docs/api/modules/jinbase/store/stack/class-Stack.md#is_empty): Tells whether the store is empty or not
    - [latest](/docs/api/modules/jinbase/store/stack/class-Stack.md#latest): Retrieve the datetime of the latest write operation.
    - [now](/docs/api/modules/jinbase/store/stack/class-Stack.md#now): Get the current datetime.
    - [now\_dt](/docs/api/modules/jinbase/store/stack/class-Stack.md#now_dt): Get the current datetime.
    - [peek](/docs/api/modules/jinbase/store/stack/class-Stack.md#peek): No docstring.
    - [pop](/docs/api/modules/jinbase/store/stack/class-Stack.md#pop): No docstring.
    - [push](/docs/api/modules/jinbase/store/stack/class-Stack.md#push): No docstring.
    - [push\_many](/docs/api/modules/jinbase/store/stack/class-Stack.md#push_many): No docstring.
    - [read\_transaction](/docs/api/modules/jinbase/store/stack/class-Stack.md#read_transaction): Context manager for executing a Read transaction.
    - [top\_uid](/docs/api/modules/jinbase/store/stack/class-Stack.md#top_uid): No docstring.
    - [transaction](/docs/api/modules/jinbase/store/stack/class-Stack.md#transaction): Context manager for executing a transaction.
    - [write\_transaction](/docs/api/modules/jinbase/store/stack/class-Stack.md#write_transaction): Context manager for executing a Write transaction.
    - [\_delete\_record](/docs/api/modules/jinbase/store/stack/class-Stack.md#_delete_record): No docstring.
    - [\_get\_top](/docs/api/modules/jinbase/store/stack/class-Stack.md#_get_top): No docstring.
    - [\_retrieve\_data](/docs/api/modules/jinbase/store/stack/class-Stack.md#_retrieve_data): No docstring.
    - [\_store\_data](/docs/api/modules/jinbase/store/stack/class-Stack.md#_store_data): No docstring.

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>
