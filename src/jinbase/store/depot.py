"""The Depot store is defined in this module."""
from contextlib import contextmanager
from paradict import Datatype, unpack
from jinbase import queries, misc
from jinbase.const import Model
from jinbase.store import Store, RecordInfo
from jinbase.blob import Blob


__all__ = ["Depot"]


class Depot(Store):
    """
    This class represents the Depot store.
    Note that a Depot object isn't intended to be directly
    instantiated by the user.
    """
    def __init__(self, jinbase):
        """
        Init

        [params]
        - jinbase: Jinbase object
        """
        super().__init__(Model.DEPOT, jinbase)

    def exists(self, uid):
        r = self._get_record(uid)
        if r is None:  # nonexistent
            return False
        return True

    def info(self, uid):
        # returns a paradict.Datatype instance + creation datetime
        r = self._get_record(uid)
        if r is None:  # nonexistent
            return
        datatype, db_timestamp = r
        created_at = misc.get_datetime_str(self._db_epoch, db_timestamp,
                                           self._timestamp_precision)
        return RecordInfo(uid=uid, datatype=datatype, created_at=created_at)

    def get(self, uid, default=None):
        with self._dbc.transaction():
            r = self._get_record(uid)  # read
            if r is None:  # nonexistent
                return default
            datatype, _ = r
            return self._retrieve_data(uid, datatype)  # read

    def get_first(self, default=None):
        with self._dbc.transaction() as cursor:
            uid = self.uid(0)
            if uid is None:
                return default
            return self.get(uid, default=default)

    def get_last(self, default=None):
        with self._dbc.transaction() as cursor:
            uid = self.uid(-1)
            if uid is None:
                return default
            return self.get(uid, default=default)

    def append(self, value):
        if value is None:
            return
        with self._dbc.immediate_transaction() as cursor:
            value = self._type_ref.adapt(value)
            datatype = misc.ensure_datatype(value, self._type_ref)
            if datatype is None:
                raise TypeError
            sql = queries.APPEND_TO_DEPOT
            db_timestamp = misc.get_timestamp(self._db_epoch, misc.now_dt(),
                                              self._timestamp_precision)
            cursor.execute(sql, (datatype.value, db_timestamp))  # write
            record_id = cursor.lastrowid
            self._store_data(record_id, datatype, value)  # write
            return record_id

    def extend(self, values):
        with self._dbc.immediate_transaction() as cursor:
            uids = list()
            for value in values:
                uid = self.append(value)  #writeS
                uids.append(uid)
            return tuple(uids)

    def uid(self, position):
        with self._dbc.transaction() as cursor:
            try:
                position = _ensure_position(self, position)  # possible read
            except IndexError as e:
                return
            r = self._get_record_by_position(position)  # read
            if r is None:
                return
            record_id, _, _ = r
            return record_id

    def position(self, uid):
        with self._dbc.transaction() as cursor:
            if not self.exists(uid):
                return
            sql = queries.COUNT_DEPOT_RECORD_OFFSET
            cursor.execute(sql, (uid,))
            r = cursor.fetchone()[0]
            return r - 1

    def uids(self, *, time_range=None, limit=None, asc=True):
        with self._dbc.cursor() as cur:
            if time_range is None:
                start, stop = 0, misc.get_timestamp(self._db_epoch, misc.now_dt(),
                                                   self._timestamp_precision)
            else:
                timestamps = misc.time_range_to_timestamps(self._db_epoch, time_range,
                                                           self._timestamp_precision)
                start, stop = timestamps
            # retrieve uids
            sort_order = "ASC" if asc else "DESC"
            limit = misc.get_limit_spec(limit)
            sql = queries.GET_DEPOT_RECORDS_BETWEEN_TIMESTAMPS.format(sort_order=sort_order,
                                                                      limit=limit)
            cur.execute(sql, (start, stop))
            for row in cur.fetch():
                uid = row[0]
                yield uid

    def iterate(self, *, time_range=None, limit=None, asc=True):
        for uid in self.uids(time_range=time_range, limit=limit, asc=asc):
            yield uid, self.get(uid)

    def count_bytes(self, uid=None):
        if uid is None:
            return super().count_bytes()
        with self._dbc.transaction() as cur:
            r = self._get_record(uid)  # read
            if r is None:
                return 0
            sql = queries.COUNT_RECORD_BYTES.format(model=self._model_name)
            cur.execute(sql, (uid,))  # read
            r = cur.fetchone()[0]
            return r if r else 0

    def count_chunks(self, uid=None):
        if uid is None:
            return super().count_chunks()
        with self._dbc.transaction() as cur:
            r = self._get_record(uid)  # read
            if r is None:
                return 0
            sql = queries.COUNT_RECORD_CHUNKS.format(model=self._model_name)
            cur.execute(sql, (uid,))  # read
            r = cur.fetchone()[0]
            return r if r else 0

    @contextmanager
    def open_blob(self, uid):
        with self._dbc.transaction() as cursor:
            n_chunks = self.count_chunks(uid)
            n_bytes = self.count_bytes(uid)
            blob = Blob(self, uid, n_bytes, n_chunks)
            try:
                yield blob
            finally:
                blob.close()

    def load_field(self, uid, field, default=None):
        with self._dbc.transaction() as cur:
            sql = queries.GET_POINTER.format(model=self._model_name)
            cur.execute(sql, (field, uid))  # read
            r = cur.fetchone()
            if r is None:
                return default
            slice_obj = slice(*r)
            with self.open_blob(uid) as blob:
                data = blob[slice_obj]
                return unpack(data)

    def fields(self):
        with self._dbc.transaction() as cur:
            sql = queries.GET_POINTED_FIELDS.format(model=self._model_name)
            cur.execute(sql)  # read
            for r in cur.fetch():
                yield r[0]

    def delete(self, uid):
        with self._dbc.immediate_transaction() as cursor:
            n = self._delete_record(uid)  # write
            return True if n > 0 else False

    def delete_many(self, uids):
        with self._dbc.immediate_transaction() as cursor:
            deleted_uids = list()
            for uid in uids:
                if self.delete(uid):
                    deleted_uids.append(uid)
            return tuple(deleted_uids)

    def _get_record(self, uid):
        with self._dbc.cursor() as cur:
            sql = queries.GET_DEPOT_RECORD
            cur.execute(sql, (uid,))
            r = cur.fetchone()
            if r is None:  # nonexistent
                return
            dtype, db_timestamp = r
            return Datatype(dtype), db_timestamp

    def _get_record_by_position(self, position):
        with self._dbc.cursor() as cur:
            sql = queries.GET_DEPOT_RECORD_BY_POSITION.format(offset=position)
            cur.execute(sql)
            r = cur.fetchone()
            if r is None:  # nonexistent
                return
            record_id, dtype, db_timestamp = r
            return record_id, Datatype(dtype), db_timestamp


def _ensure_position(store, position):
    position = int(position)
    if position >= 0:
        return position
    n = store.count_records()
    abs_position = abs(position)
    if abs_position > n:
        raise IndexError
    return n - abs_position
