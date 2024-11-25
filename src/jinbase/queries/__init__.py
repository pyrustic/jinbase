"""All SQL queries are defined in this module."""


__all__ = []


# Init script
INIT_SCRIPT = """

-- Create the JINBASE_INFO table
CREATE TABLE IF NOT EXISTS jinbase_info (
    id INTEGER NOT NULL UNIQUE DEFAULT 0,
    version INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    chunk_size INTEGER NOT NULL,
    timestamp_precision INTEGER NOT NULL,
    CONSTRAINT chk_id 
        CHECK (id == 0));
        

-- Create the JINBASE_KV_RECORD table
CREATE TABLE IF NOT EXISTS jinbase_kv_record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datatype INTEGER NOT NULL,
    timestamp INTEGER NOT NULL,
    int_key INTEGER UNIQUE,
    str_key TEXT UNIQUE,
    CONSTRAINT chk_key 
        CHECK ((int_key IS NULL AND str_key IS NOT NULL) 
              OR
              (int_key IS NOT NULL AND str_key IS NULL)));
    
-- Create index for JINBASE_KV_RECORD's timestamp
CREATE INDEX IF NOT EXISTS idx_jinbase_kv_record_timestamp 
    ON jinbase_kv_record (timestamp);

-- Create the JINBASE_KV_DATA table
CREATE TABLE IF NOT EXISTS jinbase_kv_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER NOT NULL,
    chunk BLOB NOT NULL,
    CONSTRAINT fk_jinbase_kv_data_record_id
        FOREIGN KEY (record_id) 
            REFERENCES jinbase_kv_record(id) 
                ON DELETE CASCADE);

-- Create index for JINBASE_KV_DATA's record_id
CREATE INDEX IF NOT EXISTS idx_jinbase_kv_data_record_id 
    ON jinbase_kv_data (record_id);

-- Create the JINBASE_KV_POINTER table
CREATE TABLE IF NOT EXISTS jinbase_kv_pointer (
    field TEXT NOT NULL,
    record_id INTEGER NOT NULL,
    slice_start INTEGER NOT NULL,
    slice_stop INTEGER NOT NULL,
    PRIMARY KEY (field, record_id),
    CONSTRAINT fk_jinbase_kv_pointer_record_id
        FOREIGN KEY (record_id) 
            REFERENCES jinbase_kv_record(id) 
                ON DELETE CASCADE);

-- Create index for JINBASE_KV_POINTER's record_id
CREATE INDEX IF NOT EXISTS idx_jinbase_kv_pointer_record_id 
    ON jinbase_kv_pointer (record_id);


-- Create the JINBASE_DEPOT_RECORD table
CREATE TABLE IF NOT EXISTS jinbase_depot_record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datatype INTEGER NOT NULL,
    timestamp INTEGER NOT NULL);
    
-- Create index for JINBASE_DEPOT_RECORD's timestamp
CREATE INDEX IF NOT EXISTS idx_jinbase_depot_record_timestamp 
    ON jinbase_depot_record (timestamp);

-- Create the JINBASE_DEPOT_DATA table
CREATE TABLE IF NOT EXISTS jinbase_depot_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER NOT NULL,
    chunk BLOB NOT NULL,
    CONSTRAINT fk_jinbase_depot_data_record_id
        FOREIGN KEY (record_id) 
            REFERENCES jinbase_depot_record(id) 
                ON DELETE CASCADE);

-- Create index for JINBASE_DEPOT_DATA's record_id
CREATE INDEX IF NOT EXISTS idx_jinbase_depot_data_record_id 
    ON jinbase_depot_data (record_id);

-- Create the JINBASE_DEPOT_POINTER table
CREATE TABLE IF NOT EXISTS jinbase_depot_pointer (
    field TEXT NOT NULL,
    record_id INTEGER NOT NULL,
    slice_start INTEGER NOT NULL,
    slice_stop INTEGER NOT NULL,
    PRIMARY KEY (field, record_id),
    CONSTRAINT fk_jinbase_depot_pointer_record_id
        FOREIGN KEY (record_id) 
            REFERENCES jinbase_depot_record(id) 
                ON DELETE CASCADE);

-- Create index for JINBASE_DEPOT_POINTER's record_id
CREATE INDEX IF NOT EXISTS idx_jinbase_depot_pointer_record_id 
    ON jinbase_depot_pointer (record_id);


-- Create the JINBASE_QUEUE_RECORD table
CREATE TABLE IF NOT EXISTS jinbase_queue_record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datatype INTEGER NOT NULL,
    timestamp INTEGER NOT NULL);

-- Create index for JINBASE_QUEUE_RECORD's timestamp
CREATE INDEX IF NOT EXISTS idx_jinbase_queue_record_timestamp 
    ON jinbase_queue_record (timestamp);

-- Create the JINBASE_QUEUE_DATA table
CREATE TABLE IF NOT EXISTS jinbase_queue_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER NOT NULL,
    chunk BLOB NOT NULL,
    CONSTRAINT fk_jinbase_queue_data_record_id
        FOREIGN KEY (record_id) 
            REFERENCES jinbase_queue_record(id) 
                ON DELETE CASCADE);

-- Create index for JINBASE_QUEUE_DATA's record_id
CREATE INDEX IF NOT EXISTS idx_jinbase_queue_data_record_id 
    ON jinbase_queue_data (record_id); 


-- Create the JINBASE_STACK_RECORD table
CREATE TABLE IF NOT EXISTS jinbase_stack_record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datatype INTEGER NOT NULL,
    timestamp INTEGER NOT NULL);
    
-- Create index for JINBASE_STACK_RECORD's timestamp
CREATE INDEX IF NOT EXISTS idx_jinbase_stack_record_timestamp 
    ON jinbase_stack_record (timestamp);

-- Create the JINBASE_STACK_DATA table
CREATE TABLE IF NOT EXISTS jinbase_stack_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER NOT NULL,
    chunk BLOB NOT NULL,
    CONSTRAINT fk_jinbase_stack_data_record_id
        FOREIGN KEY (record_id) 
            REFERENCES jinbase_stack_record(id) 
                ON DELETE CASCADE);
                
-- Create index for JINBASE_STACK_DATA's record_id
CREATE INDEX IF NOT EXISTS idx_jinbase_stack_data_record_id 
    ON jinbase_stack_data (record_id);
"""


# PRAGMA to run at connection creation
CONNECTION_DIRECTIVES = """
PRAGMA foreign_keys=ON;
PRAGMA synchronous=NORMAL;
"""


# Jinbase info
GET_JINBASE_INFO = """
SELECT version, created_at, chunk_size, timestamp_precision FROM jinbase_info
"""
SET_JINBASE_INFO = """
INSERT INTO jinbase_info (version, created_at, chunk_size, timestamp_precision) 
    VALUES (?, ?, ?, ?)
"""


# Record management
LATEST_WRITE = """
SELECT timestamp FROM jinbase_{model}_record ORDER BY timestamp DESC LIMIT 1
"""
COUNT_RECORDS = """
SELECT COUNT(*) AS n FROM jinbase_{model}_record
"""
RETRIEVE_RECORDS = """
SELECT id FROM jinbase_{model}_record WHERE ORDER BY id
"""
DELETE_RECORD = """
DELETE FROM jinbase_{model}_record WHERE id=?
"""
DELETE_RECORDS = """
DELETE FROM jinbase_{model}_record
"""


# Data management
GET_CHUNK_ID = """
SELECT id FROM jinbase_{model}_data WHERE record_id = ? 
ORDER BY id LIMIT 1 OFFSET {offset}
"""
STORE_DATA = """
INSERT INTO jinbase_{model}_data (record_id, chunk) VALUES (?, ?)
"""
RETRIEVE_DATA = """
SELECT chunk FROM jinbase_{model}_data WHERE record_id=? ORDER BY id
"""
COUNT_STORE_CHUNKS = """SELECT COUNT(*) AS n FROM jinbase_{model}_data
"""
COUNT_STORE_BYTES = """
SELECT SUM(LENGTH(chunk)) AS n FROM jinbase_{model}_data
"""
COUNT_RECORD_BYTES = """
SELECT SUM(LENGTH(chunk)) AS n FROM jinbase_{model}_data WHERE record_id = ?
"""
COUNT_RECORD_CHUNKS = """
SELECT COUNT(*) AS n FROM jinbase_{model}_data WHERE record_id = ?
"""

# Pointer management
ADD_POINTER = """
INSERT INTO jinbase_{model}_pointer (field, record_id, slice_start, slice_stop) 
VALUES (?, ?, ?, ?)
"""
GET_POINTER = """
SELECT slice_start, slice_stop FROM jinbase_{model}_pointer WHERE field = ? AND record_id = ?
"""
GET_POINTED_FIELDS = """
SELECT field FROM jinbase_{model}_pointer ORDER BY field
"""


# Key-value store
COUNT_KEY_OCCURRENCE = """
SELECT COUNT(*) AS n FROM jinbase_kv_record WHERE {key_type}_key=?
"""
SET_KV_RECORD = """
INSERT INTO jinbase_kv_record (datatype, timestamp, {key_type}_key) 
    VALUES (?, ?, ?)
"""
GET_KV_RECORD_BY_KEY = """
SELECT id, datatype, timestamp FROM jinbase_kv_record WHERE {key_type}_key=?
"""
GET_KV_KEY_BY_UID = """
SELECT
    CASE
        WHEN int_key IS NOT NULL THEN int_key
        ELSE str_key
    END AS key
FROM jinbase_kv_record WHERE id=?
"""
SELECT_KEYS = """
SELECT
    CASE
        WHEN int_key IS NOT NULL THEN int_key
        ELSE str_key
    END AS key
FROM jinbase_kv_record {criteria} ORDER BY key {sort_order} {limit}
"""
SELECT_INT_KEYS = """
SELECT int_key as key
FROM jinbase_kv_record 
    WHERE int_key IS NOT NULL {criteria} 
    ORDER BY key {sort_order} {limit}
"""
SELECT_STR_KEYS = """
SELECT str_key as key
FROM jinbase_kv_record 
    WHERE str_key IS NOT NULL {criteria} 
    ORDER BY key {sort_order} {limit}
"""
SELECT_STR_KEYS_WITH_GLOB = """
SELECT str_key as key
FROM jinbase_kv_record 
    WHERE str_key IS NOT NULL AND str_key GLOB ? {criteria} 
    ORDER BY key {sort_order} {limit}
"""
KV_CRITERIA_1 = "int_key >= {val}"
KV_CRITERIA_2 = "int_key <= {val}"
KV_CRITERIA_3 = "int_key BETWEEN {first} AND {last}"
KV_CRITERIA_4 = "timestamp BETWEEN {start} AND {stop}"


# Depot store
GET_DEPOT_RECORD = """
SELECT datatype, timestamp
FROM jinbase_depot_record WHERE id = ?
"""
GET_DEPOT_RECORD_BY_POSITION = """
SELECT id, datatype, timestamp
FROM jinbase_depot_record ORDER BY id LIMIT 1 OFFSET {offset}
"""
APPEND_TO_DEPOT = """
INSERT INTO jinbase_depot_record (datatype, timestamp) VALUES (?, ?)
"""
GET_DEPOT_RECORDS_BETWEEN_TIMESTAMPS = """
SELECT id FROM jinbase_depot_record WHERE timestamp BETWEEN ? AND ?
ORDER BY id {sort_order} {limit}
"""
COUNT_DEPOT_RECORD_OFFSET = """
SELECT COUNT(*) AS n FROM jinbase_depot_record WHERE id <= ?
ORDER BY id
"""



# Queue store
GET_QUEUE_FRONT = """
SELECT id, datatype, timestamp 
FROM jinbase_queue_record ORDER BY id LIMIT 1
"""
GET_QUEUE_FRONT_UID = """
SELECT id FROM jinbase_queue_record ORDER BY id LIMIT 1
"""
GET_QUEUE_BACK = """
SELECT id, datatype, timestamp 
FROM jinbase_queue_record ORDER BY id DESC LIMIT 1
"""
GET_QUEUE_BACK_UID = """
SELECT id FROM jinbase_queue_record ORDER BY id DESC LIMIT 1
"""
ENQUEUE = """
INSERT INTO jinbase_queue_record (datatype, timestamp) VALUES (?, ?)
"""


# Stack store
STACK_PUSH = """
INSERT INTO jinbase_stack_record (datatype, timestamp) VALUES (?, ?)
"""
GET_STACK_TOP = """
SELECT id, datatype, timestamp FROM jinbase_stack_record ORDER BY id DESC LIMIT 1
"""
GET_STACK_TOP_UID = """
SELECT id FROM jinbase_stack_record ORDER BY id DESC LIMIT 1
"""
