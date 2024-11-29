"""The abstract Store class is defined in this module."""
from abc import ABC
from collections import namedtuple
from paradict import Unpacker, Packer, Datatype
from litedbc import TransactionMode
from jinbase import misc
from jinbase import queries
from jinbase.const import Model


__all__ = ["Store", "RecordInfo"]


RecordInfo = namedtuple("RecordInfo",
                        ("uid", "datatype", "created_at"))
RecordInfo.__doc__ = """\
Named tuple returned by store.info()

[params]
uid: The record id
datatype: An instance of `paradict.Datatype`
created_at: Datetime string representing the creation datetime of the record
"""


class Store(ABC):
    """Abstract Store class intended to be subclassed by the
    Kv, Depot, Queue, and Stack stores"""
    def __init__(self, model, jinbase):
        """Init.

        [params]
        - model: A Model namedtuple instance
        - jinbase: Jinbase instance
        """
        self._model = Model(model)
        self._model_name = self._model.name.lower()
        self._jinbase = jinbase
        self._db_epoch = jinbase.created_at
        self._timestamp_precision = jinbase.timestamp_precision
        self._dbc = jinbase.dbc
        self._type_ref = jinbase.type_ref
        self._chunk_size = jinbase.chunk_size

    @property
    def model(self):
        return self._model

    @property
    def jinbase(self):
        return self._jinbase

    @property
    def filename(self):
        return self._dbc.filename

    @property
    def is_readonly(self):
        return self._dbc.is_readonly

    @property
    def timeout(self):
        return self._dbc.timeout

    @property
    def type_ref(self):
        return self._jinbase.type_ref

    @property
    def chunk_size(self):
        return self._jinbase.chunk_size

    @property
    def dbc(self):
        return self._dbc

    @property
    def is_new(self):
        return self._dbc.is_new

    @property
    def in_memory(self):
        return self._dbc.in_memory

    @property
    def is_closed(self):
        return self._dbc.is_closed

    def transaction(self, transaction_mode=TransactionMode.DEFERRED):
        """
        Context manager for executing a transaction.

        [params]
        - transaction: Instance of `litedbc.TransactionMode`
        """
        return self._dbc.transaction(transaction_mode=transaction_mode)

    def read_transaction(self):
        """
        Context manager for executing a Read transaction.

        [yield]
        Yields a `litedbc.Cursor` object
        """
        return self._dbc.transaction(transaction_mode=TransactionMode.DEFERRED)

    def write_transaction(self):
        """
        Context manager for executing a Write transaction.

        [yield]
        Yields a `litedbc.Cursor` object
        """
        return self._dbc.transaction(transaction_mode=TransactionMode.IMMEDIATE)

    def count_records(self):
        """
        Count all records in the store.

        [return]
        Returns the number of records
        """
        with self._dbc.cursor() as cur:
            sql = queries.COUNT_RECORDS.format(model=self._model_name)
            cur.execute(sql)  # read
            r = cur.fetchone()[0]
            return r if r else 0

    def count_bytes(self):
        """
        Count all data bytes in the store.

        [return]
        Returns the count of data bytes"""
        with self._dbc.cursor() as cur:
            sql = queries.COUNT_STORE_BYTES.format(model=self._model_name)
            cur.execute(sql)  # read
            r = cur.fetchone()[0]
            return r if r else 0

    def count_chunks(self):
        """
        Count all data chunks in the store.

        [return]
        Returns the number of chunks"""
        with self._dbc.cursor() as cur:
            sql = queries.COUNT_STORE_CHUNKS.format(model=self._model_name)
            cur.execute(sql)  # read
            r = cur.fetchone()[0]
            return r if r else 0

    def is_empty(self):
        """
        Tells whether the store is empty or not

        [return]
        Return a boolean.
        """
        return True if self.count_records() == 0 else False

    @staticmethod
    def now():
        """
        Get the current datetime.

        [return]
        Return a datetime string.
        """
        return misc.now()

    @staticmethod
    def now_dt():
        """
        Get the current datetime.

        [return]
        Return a datetime object.
        """
        return misc.now_dt()

    def latest(self):
        """
        Retrieve the datetime of the latest write operation.

        [return]
        Return a datetime string
        """
        with self._dbc.cursor() as cur:
            sql = queries.LATEST_WRITE.format(model=self._model_name)
            cur.execute(sql)  # read
            r = cur.fetchone()
            if r is None:
                return
            db_timestamp = r[0]
            return misc.get_datetime_str(self._db_epoch, db_timestamp,
                                         self._timestamp_precision)

    def delete_all(self):
        """Delete all records in the store"""
        with self._dbc.cursor() as cur:
            sql = queries.DELETE_RECORDS.format(model=self._model_name)
            cur.execute(sql)  # write

    def _store_data(self, record_id, datatype, value):
        with self._dbc.cursor() as cur:
            sql = queries.STORE_DATA.format(model=self._model_name)
            if datatype == Datatype.BIN:
                for chunk in misc.split_bin(value, chunk_size=self._chunk_size):
                    cur.execute(sql, (record_id, chunk))
            else:
                buffer = bytearray()
                packer = Packer(type_ref=self._type_ref, auto_index=True)
                for x in packer.pack(value):
                    buffer.extend(x)
                    while len(buffer) >= self._chunk_size:
                        chunk = buffer[:self._chunk_size]
                        del buffer[:self._chunk_size]
                        cur.execute(sql, (record_id, chunk))
                if buffer:
                    cur.execute(sql, (record_id, buffer))
                # create pointers
                if datatype == Datatype.DICT and self._model in (Model.KV,
                                                                 Model.DEPOT):
                    sql = queries.ADD_POINTER.format(model=self._model_name)
                    for field, slice_obj in packer.index_dict.items():
                        if isinstance(field, str):
                            cur.execute(sql, (field,
                                              record_id,
                                              slice_obj.start,
                                              slice_obj.stop))

    def _retrieve_data(self, record_id, datatype):
        with self._dbc.cursor() as cur:
            is_serialized = False if datatype == Datatype.BIN else True
            sql = queries.RETRIEVE_DATA.format(model=self._model_name)
            chunks = bytearray()
            unpacker = Unpacker(type_ref=self._type_ref)
            cur.execute(sql, (record_id, ))
            for row in cur.fetch():
                chunk = row[0]
                if is_serialized:
                    unpacker.feed(chunk)
                else:
                    chunks.extend(chunk)
            if is_serialized:
                return unpacker.data
            else:
                return self._type_ref.bin_type(chunks)

    def _delete_record(self, record_id):
        with self._dbc.cursor() as cur:
            sql = queries.DELETE_RECORD.format(model=self._model_name)
            cur.execute(sql, (record_id, ))
            return cur.rowcount
