"""The main module of Jinbase."""
from datetime import datetime, timezone
from paradict import TypeRef
from litedbc import LiteDBC, TransactionMode
from jinbase import errors, queries, misc, const
from jinbase.store import RecordInfo
from jinbase.store.depot import Depot
from jinbase.store.kv import Kv
from jinbase.store.queue import Queue
from jinbase.store.stack import Stack
from jinbase.const import (Model, TimestampPrecision, TIMESTAMP_PRECISION,
                           TIMEOUT, CHUNK_SIZE, JINBASE_HOME, JINBASE_VERSION,
                           USER_HOME, DATETIME_FORMAT)


__all__ = ["Jinbase", "Model", "TypeRef", "RecordInfo",
           "TimestampPrecision", "TIMEOUT", "CHUNK_SIZE",
           "TIMESTAMP_PRECISION", "DATETIME_FORMAT",
           "USER_HOME", "JINBASE_HOME", "JINBASE_VERSION"]


class Jinbase:
    """The Jinbase class. A Jinbase object is intended to
    be directly instantiated by the user."""
    def __init__(self, filename=None, *, auto_create=True,
                 is_readonly=False, timeout=TIMEOUT,
                 type_ref=None, chunk_size=CHUNK_SIZE,
                 timestamp_precision=TIMESTAMP_PRECISION):
        """
        Init.

        [params]
        - filename: The filename of the Jinbase database.
            If the pointed file doesn't exist, it will be created
            if `auto_create` is set to True.
        - auto_create: Boolean to tell whether a nonexistent database file
            should automatically be created or not. Defaults to True.
        - is_readonly: Boolean to tell whether the database connection should be in
            readonly or not.
        - timeout: Timeout in seconds for all database operations.
            Defaults to the value of `jinbase.TIMEOUT`
        - type_ref: A paradict.TypeRef instance
        - chunk_size: Chunk size in bytes. Defaults to `jinbase.CHUNK_SIZE`.
            Note that this value is only relevant when the Jinbase tables are created.
        - timestamp_precision: An instance of the `jinbase.TimestampPrecision` namedtuple.
            Defaults to `jinbase.TIMESTAMP_PRECISION`.
            Note that this value is only relevant when the Jinbase tables are created.
        """
        self._dbc = create_dbc(filename, auto_create, is_readonly, timeout)
        with self._dbc.cursor() as cur:
            cur.executescript(queries.INIT_SCRIPT)
        chunk_size = int(chunk_size) if chunk_size else CHUNK_SIZE
        x = ensure_jinbase(self._dbc, chunk_size,
                           TimestampPrecision(timestamp_precision))
        self._version, self._created_at, self._chunk_size, self._timestamp_precision = x
        self._creation_dt = datetime.fromisoformat(self._created_at).astimezone(tz=timezone.utc)
        self._auto_create = auto_create
        self._filename = self._dbc.filename
        self._is_readonly = self._dbc.is_readonly
        self._timeout = self._dbc.timeout
        self._type_ref = TypeRef() if type_ref is None else type_ref
        # stores
        self._kv = Kv(self)
        self._depot = Depot(self)
        self._queue = Queue(self)
        self._stack = Stack(self)

    @property
    def kv(self):
        return self._kv

    @property
    def depot(self):
        return self._depot

    @property
    def queue(self):
        return self._queue

    @property
    def stack(self):
        return self._stack

    @property
    def filename(self):
        return self._filename

    @property
    def is_readonly(self):
        return self._is_readonly

    @property
    def timeout(self):
        return self._timeout

    @property
    def type_ref(self):
        return self._type_ref

    @property
    def chunk_size(self):
        return self._chunk_size

    @property
    def timestamp_precision(self):
        return self._timestamp_precision

    @property
    def dbc(self):
        """The instance of litedbc.LiteDBC"""
        return self._dbc

    @property
    def created_at(self):
        return self._created_at

    @property
    def creation_dt(self):
        return self._creation_dt

    @property
    def version(self):
        return self._version

    @property
    def is_new(self):
        return self._dbc.is_new

    @property
    def in_memory(self):
        return self._dbc.in_memory

    @property
    def is_closed(self):
        return self._dbc.is_closed

    @property
    def is_destroyed(self):
        return self._dbc.is_destroyed

    def scan(self):
        """
        Scan the Jinbase database

        [returns]
        A dictionary object whose keys are jinbase.Model namedtuples
        and values are tuples of the total record count and total byte count.
        """
        model2store = {Model.DEPOT: self._depot,
                       Model.KV: self._kv,
                       Model.QUEUE: self._queue,
                       Model.STACK: self._stack}
        return {model: (store.count_records(), store.count_bytes())
                for model, store in model2store.items()}

    @staticmethod
    def now():
        """
        Get the current utc datetime.

        [returns]
        A utc instance of `datetime.datetime`
        """
        return misc.now()

    @staticmethod
    def now_dt():
        """
        Get the current utc datetime.

        [returns]
        A utc string
        """
        return misc.now_dt()

    def latest(self):
        """
        Get the utc datetime of the latest operation.

        [returns]
        A utc instance of `datetime.datetime`
        """
        with self._dbc.cursor() as cur:
            timestamps = list()
            for model_name in [model.name.lower() for model in Model]:
                sql = queries.LATEST_WRITE.format(model=model_name)
                cur.execute(sql)  # read
                r = cur.fetchone()
                if r is None:
                    continue
                db_timestamp = r[0]
                timestamps.append(db_timestamp)
            db_timestamp = -1
            for t in timestamps:
                if t > db_timestamp:
                    db_timestamp = t
            if db_timestamp == -1:
                return
            db_epoch = self._created_at
            return misc.get_datetime_str(db_epoch, db_timestamp,
                                         self._timestamp_precision)

    def count_records(self):
        with self._dbc.transaction() as cursor:
            n1 = self._kv.count_records()
            n2 = self._depot.count_records()
            n3 = self._queue.count_records()
            n4 = self._stack.count_records()
            return n1 + n2 + n3 + n4

    def count_bytes(self):
        with self._dbc.transaction() as cursor:
            n1 = self._kv.count_bytes()
            n2 = self._depot.count_bytes()
            n3 = self._queue.count_bytes()
            n4 = self._stack.count_bytes()
            return n1 + n2 + n3 + n4

    def count_chunks(self):
        with self._dbc.transaction() as cursor:
            n1 = self._kv.count_chunks()
            n2 = self._depot.count_chunks()
            n3 = self._queue.count_chunks()
            n4 = self._stack.count_chunks()
            return n1 + n2 + n3 + n4

    def transaction(self, transaction_mode=TransactionMode.DEFERRED):
        return self._dbc.transaction(transaction_mode=transaction_mode)

    def read_transaction(self):
        return self._dbc.transaction(transaction_mode=TransactionMode.DEFERRED)

    def write_transaction(self):
        return self._dbc.transaction(transaction_mode=TransactionMode.IMMEDIATE)

    def vacuum(self):
        """Vacuum the database"""
        self._dbc.vacuum()

    def vacuum_into(self, dst):
        """Vacuum into a file whose name is provided via `dst`."""
        self._dbc.vacuum_into(dst)

    def set_locking_mode(self, locking_mode):
        return self._dbc.set_locking_mode(locking_mode)

    def get_locking_mode(self):
        return self._dbc.get_locking_mode()

    def set_sync_mode(self, sync_mode):
        return self._dbc.set_sync_mode(sync_mode)

    def get_sync_mode(self):
        return self._dbc.get_sync_mode()

    def set_journal_mode(self, journal_mode):
        return self._dbc.set_journal_mode(journal_mode)

    def get_journal_mode(self):
        return self._dbc.get_journal_mode()

    def set_progress_handler(self, callback, n):
        return self._dbc.set_progress_handler(callback, n)

    def set_trace_callback(self, callback):
        return self._dbc.set_trace_callback(callback)

    def interrupt(self):
        return self._dbc.interrupt()

    def backup(self, dst, *, pages=-1,
               progress=None, sleep=0.250):
        self._dbc.backup(dst, pages=pages, progress=progress,
                         sleep=sleep)

    def iterdump(self):
        """Returns an iterator to the dump of the database
         in an SQL text format"""
        return self._dbc.iterdump()

    def copy(self):
        """Create a new Jinbase instance that
        points to the same database file"""
        return self.__copy__()

    def close(self):
        """Close the connection"""
        return self._dbc.close()

    def destroy(self):
        """Destroy the database file"""
        return self._dbc.destroy()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __copy__(self):
        return Jinbase(self._filename, auto_create=self._auto_create,
                       is_readonly=self._is_readonly, timeout=self._timeout,
                       type_ref=self._type_ref, chunk_size=self._chunk_size)


def create_dbc(filename, auto_create, is_readonly, timeout):
    def on_create_conn(dbc):
        with dbc.cursor() as cur:
            cur.executescript(queries.CONNECTION_DIRECTIVES,
                              transaction_mode=None)
    dbc = LiteDBC(filename, auto_create=auto_create,
                  is_readonly=is_readonly, timeout=timeout,
                  on_create_conn=on_create_conn)
    return dbc


def ensure_jinbase(dbc, chunk_size, timestamp_precision):
    sql = queries.GET_JINBASE_INFO
    if dbc.is_readonly:
        with dbc.cursor() as cur:
            cur.execute(sql)
            r = cur.fetchone()
            if r is None:
                msg = "Not a Jinbase file."
                raise Exception(msg)
            else:
                version, created_at, chunk_size, timestamp_precision = r
            return version, created_at, chunk_size, TimestampPrecision(timestamp_precision)
    else:
        with dbc.immediate_transaction() as cursor:
            sql = queries.GET_JINBASE_INFO
            cursor.execute(sql)
            r = cursor.fetchone()
            if r is None:
                sql = queries.SET_JINBASE_INFO
                version = const.JINBASE_VERSION
                created_at = misc.now()
                cursor.execute(sql, (version, created_at, chunk_size,
                                     timestamp_precision.value))
            else:
                version, created_at, chunk_size, timestamp_precision = r
            return version, created_at, chunk_size, TimestampPrecision(timestamp_precision)
