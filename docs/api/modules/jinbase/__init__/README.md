###### Jinbase API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | Module | [Source](/src/jinbase/__init__.py)

# Module Overview
> Module: **jinbase.\_\_init\_\_**

The main module of Jinbase.

## Fields
- [**All fields**](/docs/api/modules/jinbase/__init__/fields.md)
    - CHUNK\_SIZE = `1048576`
    - DATETIME\_FORMAT = `'%Y-%m-%d %H:%M:%S.%fZ'`
    - JINBASE\_HOME = `'/home/alex/JinbaseHome'`
    - JINBASE\_VERSION = `1`
    - TIMEOUT = `5.0`
    - TIMESTAMP\_PRECISION = `<TimestampPrecision.MILLISECONDS: 3>`
    - USER\_HOME = `'/home/alex'`

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>

## Classes
- [**Jinbase**](/docs/api/modules/jinbase/__init__/class-Jinbase.md): The Jinbase class. A Jinbase object is intended to be directly instantiated by the user.
    - [chunk\_size](/docs/api/modules/jinbase/__init__/class-Jinbase.md#properties-table); _getter_
    - [created\_at](/docs/api/modules/jinbase/__init__/class-Jinbase.md#properties-table); _getter_
    - [creation\_dt](/docs/api/modules/jinbase/__init__/class-Jinbase.md#properties-table); _getter_
    - [dbc](/docs/api/modules/jinbase/__init__/class-Jinbase.md#properties-table); _getter_
    - [depot](/docs/api/modules/jinbase/__init__/class-Jinbase.md#properties-table); _getter_
    - [filename](/docs/api/modules/jinbase/__init__/class-Jinbase.md#properties-table); _getter_
    - [in\_memory](/docs/api/modules/jinbase/__init__/class-Jinbase.md#properties-table); _getter_
    - [is\_closed](/docs/api/modules/jinbase/__init__/class-Jinbase.md#properties-table); _getter_
    - [is\_destroyed](/docs/api/modules/jinbase/__init__/class-Jinbase.md#properties-table); _getter_
    - [is\_new](/docs/api/modules/jinbase/__init__/class-Jinbase.md#properties-table); _getter_
    - [is\_readonly](/docs/api/modules/jinbase/__init__/class-Jinbase.md#properties-table); _getter_
    - [kv](/docs/api/modules/jinbase/__init__/class-Jinbase.md#properties-table); _getter_
    - [queue](/docs/api/modules/jinbase/__init__/class-Jinbase.md#properties-table); _getter_
    - [stack](/docs/api/modules/jinbase/__init__/class-Jinbase.md#properties-table); _getter_
    - [timeout](/docs/api/modules/jinbase/__init__/class-Jinbase.md#properties-table); _getter_
    - [timestamp\_precision](/docs/api/modules/jinbase/__init__/class-Jinbase.md#properties-table); _getter_
    - [type\_ref](/docs/api/modules/jinbase/__init__/class-Jinbase.md#properties-table); _getter_
    - [version](/docs/api/modules/jinbase/__init__/class-Jinbase.md#properties-table); _getter_
    - [backup](/docs/api/modules/jinbase/__init__/class-Jinbase.md#backup): No docstring.
    - [close](/docs/api/modules/jinbase/__init__/class-Jinbase.md#close): Close the connection
    - [copy](/docs/api/modules/jinbase/__init__/class-Jinbase.md#copy): Create a new Jinbase instance that points to the same database file
    - [count\_bytes](/docs/api/modules/jinbase/__init__/class-Jinbase.md#count_bytes): No docstring.
    - [count\_chunks](/docs/api/modules/jinbase/__init__/class-Jinbase.md#count_chunks): No docstring.
    - [count\_records](/docs/api/modules/jinbase/__init__/class-Jinbase.md#count_records): No docstring.
    - [destroy](/docs/api/modules/jinbase/__init__/class-Jinbase.md#destroy): Destroy the database file
    - [get\_journal\_mode](/docs/api/modules/jinbase/__init__/class-Jinbase.md#get_journal_mode): No docstring.
    - [get\_locking\_mode](/docs/api/modules/jinbase/__init__/class-Jinbase.md#get_locking_mode): No docstring.
    - [get\_sync\_mode](/docs/api/modules/jinbase/__init__/class-Jinbase.md#get_sync_mode): No docstring.
    - [interrupt](/docs/api/modules/jinbase/__init__/class-Jinbase.md#interrupt): No docstring.
    - [iterdump](/docs/api/modules/jinbase/__init__/class-Jinbase.md#iterdump): Returns an iterator to the dump of the database in an SQL text format
    - [latest](/docs/api/modules/jinbase/__init__/class-Jinbase.md#latest): Get the utc datetime of the latest operation.
    - [now](/docs/api/modules/jinbase/__init__/class-Jinbase.md#now): Get the current utc datetime.
    - [now\_dt](/docs/api/modules/jinbase/__init__/class-Jinbase.md#now_dt): Get the current utc datetime.
    - [read\_transaction](/docs/api/modules/jinbase/__init__/class-Jinbase.md#read_transaction): No docstring.
    - [scan](/docs/api/modules/jinbase/__init__/class-Jinbase.md#scan): Scan the Jinbase database
    - [set\_journal\_mode](/docs/api/modules/jinbase/__init__/class-Jinbase.md#set_journal_mode): No docstring.
    - [set\_locking\_mode](/docs/api/modules/jinbase/__init__/class-Jinbase.md#set_locking_mode): No docstring.
    - [set\_progress\_handler](/docs/api/modules/jinbase/__init__/class-Jinbase.md#set_progress_handler): No docstring.
    - [set\_sync\_mode](/docs/api/modules/jinbase/__init__/class-Jinbase.md#set_sync_mode): No docstring.
    - [set\_trace\_callback](/docs/api/modules/jinbase/__init__/class-Jinbase.md#set_trace_callback): No docstring.
    - [transaction](/docs/api/modules/jinbase/__init__/class-Jinbase.md#transaction): No docstring.
    - [vacuum](/docs/api/modules/jinbase/__init__/class-Jinbase.md#vacuum): Vacuum the database
    - [vacuum\_into](/docs/api/modules/jinbase/__init__/class-Jinbase.md#vacuum_into): Vacuum into a file whose name is provided via `dst`.
    - [write\_transaction](/docs/api/modules/jinbase/__init__/class-Jinbase.md#write_transaction): No docstring.
- [**Model**](/docs/api/modules/jinbase/__init__/class-Model.md): Create a collection of name/value pairs.
    - KV = `1`
    - DEPOT = `2`
    - QUEUE = `3`
    - STACK = `4`
- [**RecordInfo**](/docs/api/modules/jinbase/__init__/class-RecordInfo.md): Named tuple returned by store.info()
    - uid: Alias for field number 0
    - datatype: Alias for field number 1
    - created\_at: Alias for field number 2
- [**TimestampPrecision**](/docs/api/modules/jinbase/__init__/class-TimestampPrecision.md): Create a collection of name/value pairs.
    - SECONDS = `0`
    - MILLISECONDS = `3`
    - MICROSECONDS = `6`
    - NANOSECONDS = `9`
- [**TypeRef**](/docs/api/modules/jinbase/__init__/class-TypeRef.md): This class represents a mechanism for customizing Python types allowed for (de)serializing data with Paradict classes and functi...
    - [adapters](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [bin\_type](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [bin\_types](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [bool\_type](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [bool\_types](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [complex\_type](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [complex\_types](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [date\_type](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [date\_types](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [datetime\_type](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [datetime\_types](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [dict\_type](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [dict\_types](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [float\_type](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [float\_types](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [grid\_type](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [grid\_types](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [int\_type](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [int\_types](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [list\_type](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [list\_types](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [obj\_type](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [obj\_types](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [set\_type](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [set\_types](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [str\_type](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [str\_types](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [time\_type](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [time\_types](/docs/api/modules/jinbase/__init__/class-TypeRef.md#properties-table); _getter, setter_
    - [adapt](/docs/api/modules/jinbase/__init__/class-TypeRef.md#adapt): Checks the 'adapters' attribute to find out if there is an adapter function registered for the type of the data argument. Then, ...
    - [check](/docs/api/modules/jinbase/__init__/class-TypeRef.md#check): This function accepts as argument a Python type, and return a Datatype instance if the type is supported/registered, else return...
    - [\_create\_map](/docs/api/modules/jinbase/__init__/class-TypeRef.md#_create_map): No docstring.
    - [\_update\_types](/docs/api/modules/jinbase/__init__/class-TypeRef.md#_update_types): No docstring.

<p align="right"><a href="#jinbase-api-reference">Back to top</a></p>
