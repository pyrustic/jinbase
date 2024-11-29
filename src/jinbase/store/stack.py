"""The Stack store is defined in this module."""
from paradict import Datatype
from jinbase import queries, misc
from jinbase.const import Model
from jinbase.store import Store, RecordInfo


__all__ = ["Stack"]


class Stack(Store):
    """
    This class represents the Stack store.
    Note that a Stack object isn't intended to be directly
    instantiated by the user.
    """
    def __init__(self, jinbase):
        """
        Init

        [params]
        - jinbase: Jinbase object
        """
        super().__init__(Model.STACK, jinbase)

    def push(self, value):
        if value is None:
            return
        with self._dbc.immediate_transaction() as cursor:
            value = self._type_ref.adapt(value)
            datatype = misc.ensure_datatype(value, self._type_ref)
            if datatype is None:
                raise TypeError
            sql = queries.STACK_PUSH
            db_timestamp = misc.get_timestamp(self._db_epoch, misc.now_dt(),
                                              self._timestamp_precision)
            cursor.execute(sql, (datatype.value, db_timestamp))  # write
            record_id = cursor.lastrowid
            self._store_data(record_id, datatype, value)  # write
            return record_id

    def push_many(self, values):
        with self._dbc.immediate_transaction() as cursor:
            uids = list()
            for value in values:
                uid = self.push(value)
                uids.append(uid)
            return tuple(uids)

    def pop(self, default=None):
        with self._dbc.immediate_transaction() as cursor:
            r = self._get_top()  # read
            if r is None:
                return default
            record_id, datatype, _ = r
            # get value
            value = self._retrieve_data(record_id, datatype)  # read
            # delete record
            self._delete_record(record_id)
            return value

    def peek(self, default=None):
        with self._dbc.transaction():
            r = self._get_top()  # read
            if r is None:
                return default
            record_id, datatype, _ = r
            return self._retrieve_data(record_id, datatype)

    def top_uid(self):
        with self._dbc.cursor() as cur:
            sql = queries.GET_STACK_TOP_UID
            cur.execute(sql)
            r = cur.fetchone()
            if r is None:
                return
            return r[0]

    def count_top_bytes(self):
        with self._dbc.transaction() as cur:
            r = self._get_top()  # read
            if r is None:
                return 0
            record_id, _, _ = r
            sql = queries.COUNT_RECORD_BYTES.format(model=self._model_name)
            cur.execute(sql, (record_id,))  # read
            r = cur.fetchone()[0]
            return r if r else 0

    def count_top_chunks(self):
        with self._dbc.transaction() as cur:
            r = self._get_top()  # read
            if r is None:
                return 0
            record_id, _, _ = r
            sql = queries.COUNT_RECORD_CHUNKS.format(model=self._model_name)
            cur.execute(sql, (record_id,))  # read
            r = cur.fetchone()[0]
            return r if r else 0

    def info_top(self):
        r = self._get_top()  # read
        if r is None:
            return
        record_id, datatype, db_timestamp = r
        created_at = misc.get_datetime_str(self._db_epoch, db_timestamp,
                                           self._timestamp_precision)
        return RecordInfo(uid=record_id, datatype=datatype, created_at=created_at)

    def _get_top(self):
        with self._dbc.cursor() as cur:
            sql = queries.GET_STACK_TOP
            cur.execute(sql)
            r = cur.fetchone()
            if r is None:
                return
            record_id, dtype, db_timestamp = r
            return record_id, Datatype(dtype), db_timestamp
