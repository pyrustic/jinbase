###### Jinbase API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | Module | [Source](/src/jinbase/store/queue.py)

# Module Overview
> Module: **jinbase.store.queue**

The Queue store is defined in this module.

## Classes
- [**Queue**](/docs/api/modules/jinbase/store/queue/class-Queue.md): This class represents the Queue store. Note that a Queue object isn't intended to be directly instantiated by the user.
    - [\_abc\_impl](/docs/api/modules/jinbase/store/queue/class-Queue.md#fields-table) = `<_abc._abc_data object at 0x789010e46240>`
    - [chunk\_size](/docs/api/modules/jinbase/store/queue/class-Queue.md#properties-table); _getter_
    - [dbc](/docs/api/modules/jinbase/store/queue/class-Queue.md#properties-table); _getter_
    - [filename](/docs/api/modules/jinbase/store/queue/class-Queue.md#properties-table); _getter_
    - [in\_memory](/docs/api/modules/jinbase/store/queue/class-Queue.md#properties-table); _getter_
    - [is\_closed](/docs/api/modules/jinbase/store/queue/class-Queue.md#properties-table); _getter_
    - [is\_new](/docs/api/modules/jinbase/store/queue/class-Queue.md#properties-table); _getter_
    - [is\_readonly](/docs/api/modules/jinbase/store/queue/class-Queue.md#properties-table); _getter_
    - [jinbase](/docs/api/modules/jinbase/store/queue/class-Queue.md#properties-table); _getter_
    - [model](/docs/api/modules/jinbase/store/queue/class-Queue.md#properties-table); _getter_
    - [timeout](/docs/api/modules/jinbase/store/queue/class-Queue.md#properties-table); _getter_
    - [type\_ref](/docs/api/modules/jinbase/store/queue/class-Queue.md#properties-table); _getter_
    - [back\_uid](/docs/api/modules/jinbase/store/queue/class-Queue.md#back_uid): No docstring.
    - [count\_back\_bytes](/docs/api/modules/jinbase/store/queue/class-Queue.md#count_back_bytes): No docstring.
    - [count\_back\_chunks](/docs/api/modules/jinbase/store/queue/class-Queue.md#count_back_chunks): No docstring.
    - [count\_bytes](/docs/api/modules/jinbase/store/queue/class-Queue.md#count_bytes): Count all data bytes in the store.
    - [count\_chunks](/docs/api/modules/jinbase/store/queue/class-Queue.md#count_chunks): Count all data chunks in the store.
    - [count\_front\_bytes](/docs/api/modules/jinbase/store/queue/class-Queue.md#count_front_bytes): No docstring.
    - [count\_front\_chunks](/docs/api/modules/jinbase/store/queue/class-Queue.md#count_front_chunks): No docstring.
    - [count\_records](/docs/api/modules/jinbase/store/queue/class-Queue.md#count_records): Count all records in the store.
    - [delete\_all](/docs/api/modules/jinbase/store/queue/class-Queue.md#delete_all): Delete all records in the store
    - [dequeue](/docs/api/modules/jinbase/store/queue/class-Queue.md#dequeue): No docstring.
    - [enqueue](/docs/api/modules/jinbase/store/queue/class-Queue.md#enqueue): No docstring.
    - [enqueue\_many](/docs/api/modules/jinbase/store/queue/class-Queue.md#enqueue_many): No docstring.
    - [front\_uid](/docs/api/modules/jinbase/store/queue/class-Queue.md#front_uid): No docstring.
    - [info\_back](/docs/api/modules/jinbase/store/queue/class-Queue.md#info_back): No docstring.
    - [info\_front](/docs/api/modules/jinbase/store/queue/class-Queue.md#info_front): No docstring.
    - [is\_empty](/docs/api/modules/jinbase/store/queue/class-Queue.md#is_empty): Tells whether the store is empty or not
    - [latest](/docs/api/modules/jinbase/store/queue/class-Queue.md#latest): Retrieve the datetime of the latest write operation.
    - [now](/docs/api/modules/jinbase/store/queue/class-Queue.md#now): Get the current datetime.
    - [now\_dt](/docs/api/modules/jinbase/store/queue/class-Queue.md#now_dt): Get the current datetime.
    - [peek\_back](/docs/api/modules/jinbase/store/queue/class-Queue.md#peek_back): No docstring.
    - [peek\_front](/docs/api/modules/jinbase/store/queue/class-Queue.md#peek_front): No docstring.
    - [read\_transaction](/docs/api/modules/jinbase/store/queue/class-Queue.md#read_transaction): Context manager for executing a Read transaction.
    - [transaction](/docs/api/modules/jinbase/store/queue/class-Queue.md#transaction): Context manager for executing a transaction.
    - [write\_transaction](/docs/api/modules/jinbase/store/queue/class-Queue.md#write_transaction): Context manager for executing a Write transaction.
    - [\_delete\_record](/docs/api/modules/jinbase/store/queue/class-Queue.md#_delete_record): No docstring.
    - [\_get\_back](/docs/api/modules/jinbase/store/queue/class-Queue.md#_get_back): No docstring.
    - [\_get\_front](/docs/api/modules/jinbase/store/queue/class-Queue.md#_get_front): No docstring.
    - [\_retrieve\_data](/docs/api/modules/jinbase/store/queue/class-Queue.md#_retrieve_data): No docstring.
    - [\_store\_data](/docs/api/modules/jinbase/store/queue/class-Queue.md#_store_data): No docstring.

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>
