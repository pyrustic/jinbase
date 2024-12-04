"""The Kv store is defined in this module."""
from contextlib import contextmanager
from paradict import Datatype, unpack
from jinbase import queries, misc
from jinbase.blob import Blob
from jinbase.const import Model
from jinbase.store import Store, RecordInfo


__all__ = ["Kv"]


class Kv(Store):
    """
    This class represents the Kv store.
    Note that a Kv object isn't intended to be directly
    instantiated by the user.
    """
    def __init__(self, jinbase):
        """
        Init

        [params]
        - jinbase: Jinbase object
        """
        super().__init__(Model.KV, jinbase)

    def exists(self, key):
        with self._dbc.cursor() as cur:
            key = _ensure_key(key)
            r = self._get_record_by_key(key)  # read
            return False if r is None else True

    def info(self, key):
        key = _ensure_key(key)
        r = self._get_record_by_key(key)
        if r is None:
            return
        record_id, datatype, db_timestamp = r
        created_at = misc.get_datetime_str(self._db_epoch, db_timestamp,
                                           self._timestamp_precision)
        return RecordInfo(uid=record_id, datatype=datatype,
                          created_at=created_at)

    def get(self, key, default=None):
        with self._dbc.transaction() as cur:
            key = _ensure_key(key)
            r = self._get_record_by_key(key)  # read
            if r is None:
                return default
            record_id, datatype, _ = r
            return self._retrieve_data(record_id, datatype)  # read

    def set(self, key, value):
        if value is None:
            return
        with self._dbc.immediate_transaction() as cursor:
            key = _ensure_key(key)
            key_type = _get_key_type(key)
            datatype = misc.ensure_datatype(value, self._type_ref)
            if datatype is None:
                raise TypeError
            sql = queries.SET_KV_RECORD.format(key_type=key_type)
            db_timestamp = misc.get_timestamp(self._db_epoch, misc.now_dt(),
                                              self._timestamp_precision)
            params = (datatype.value, db_timestamp, key)
            r = self._get_record_by_key(key)  # read
            # key doesn't exist
            if r is None:
                cursor.execute(sql, params)  # write
            # key already exists, therefore we should delete it first
            else:
                record_id, _, _ = r
                self._delete_record(record_id)  # write
                cursor.execute(sql, params)  # write
            record_id = cursor.lastrowid
            self._store_data(record_id, datatype, value)  # write
            return record_id

    def replace(self, key, value):
        with self._dbc.immediate_transaction() as cursor:
            old_value = self.get(key)
            if old_value is None:
                return
            if not self.set(key, value):
                return
            return old_value

    def update(self, dict_data):
        """data is a dictionary"""
        data = dict(dict_data)
        with self._dbc.immediate_transaction() as cursor:
            uids = dict()
            for key, val in data.items():
                uid = self.set(key, val)  # writeS
                uids[key] = uid
            return uids

    def keys(self, *, time_range=None, limit=None, asc=True):
        with self._dbc.cursor() as cur:
            sort_order = "ASC" if asc else "DESC"
            if time_range is None:
                timestamps = None
            else:
                timestamps = misc.time_range_to_timestamps(self._db_epoch, time_range,
                                                           self._timestamp_precision)
            criteria = _get_key_criteria(timestamps)
            limit = misc.get_limit_spec(limit)
            sql = queries.SELECT_KEYS.format(sort_order=sort_order,
                                             criteria=criteria,
                                             limit=limit)
            cur.execute(sql)  # read
            for row in cur.fetch():
                yield row[0]

    def int_keys(self, first=None, last=None, *, time_range=None, limit=None,
                 asc=True):
        with self._dbc.cursor() as cur:
            first = first if first is None else int(first)
            last = last if last is None else int(last)
            if first is not None and last is not None and first > last:
                x = first
                first = last
                last = x
            sort_order = "ASC" if asc else "DESC"
            if time_range is None:
                timestamps = None
            else:
                timestamps = misc.time_range_to_timestamps(self._db_epoch, time_range,
                                                           self._timestamp_precision)
            criteria = _get_int_key_criteria(first, last, timestamps)
            limit = misc.get_limit_spec(limit)
            sql = queries.SELECT_INT_KEYS.format(sort_order=sort_order,
                                                 criteria=criteria, limit=limit)
            cur.execute(sql)
            for row in cur.fetch():
                yield row[0]

    def str_keys(self, glob=None, *, time_range=None, limit=None, asc=True):
        if glob is not None and not isinstance(glob, str):
            msg = "The Glob should be a string"
            raise Exception(msg)
        with self._dbc.cursor() as cur:
            sort_order = "ASC" if asc else "DESC"
            if time_range is None:
                timestamps = None
            else:
                timestamps = misc.time_range_to_timestamps(self._db_epoch, time_range,
                                                           self._timestamp_precision)
            criteria = _get_str_key_criteria(timestamps)
            limit = misc.get_limit_spec(limit)
            if glob:
                sql = queries.SELECT_STR_KEYS_WITH_GLOB.format(sort_order=sort_order,
                                                               criteria=criteria,
                                                               limit=limit)
                params = (glob, )
            else:
                sql = queries.SELECT_STR_KEYS.format(sort_order=sort_order,
                                                     criteria=criteria, limit=limit)
                params = None
            cur.execute(sql, params)
            for row in cur.fetch():
                yield row[0]

    def iterate(self, *, time_range=None, limit=None, asc=True):
        for key in self.keys(time_range=time_range, limit=limit, asc=asc):
            try:
                value = self[key]
            except KeyError as e:
                continue
            yield key, value

    def uid(self, key):
        key = _ensure_key(key)
        r = self._get_record_by_key(key)
        if r is None:  # nonexistent
            return
        record_id, _, _ = r
        return record_id

    def key(self, uid):
        with self._dbc.cursor() as cur:
            sql = queries.GET_KV_KEY_BY_UID
            cur.execute(sql, (uid,))
            r = cur.fetchone()
            if r is None:  # nonexistent
                return
            return r[0]

    def count_bytes(self, key=None):
        if key is None:
            return super().count_bytes()
        with self._dbc.transaction() as cur:
            key = _ensure_key(key)
            r = self._get_record_by_key(key)  # read
            if r is None:
                return 0
            record_id, _, _ = r
            sql = queries.COUNT_RECORD_BYTES.format(model=self._model_name)
            cur.execute(sql, (record_id, ))  # read
            return cur.fetchone()[0]

    def count_chunks(self, key=None):
        if key is None:
            return super().count_chunks()
        with self._dbc.transaction() as cur:
            key = _ensure_key(key)
            r = self._get_record_by_key(key)  # read
            if r is None:
                return 0
            record_id, _, _ = r
            sql = queries.COUNT_RECORD_CHUNKS.format(model=self._model_name)
            cur.execute(sql, (record_id, ))  # read
            return cur.fetchone()[0]

    @contextmanager
    def open_blob(self, key):
        with self._dbc.transaction() as cursor:
            uid = self.uid(key)
            n_chunks = self.count_chunks(key)
            n_bytes = self.count_bytes(key)
            blob = Blob(self, uid, n_bytes, n_chunks)
            try:
                yield blob
            finally:
                blob.close()

    def load_field(self, key, field, default=None):
        with self._dbc.transaction() as cur:
            uid = self.uid(key)
            sql = queries.GET_POINTER.format(model=self._model_name)
            cur.execute(sql, (field, uid))  # read
            r = cur.fetchone()
            if r is None:
                return default
            slice_obj = slice(*r)
            with self.open_blob(key) as blob:
                data = blob[slice_obj]
                return unpack(data)

    def fields(self):
        with self._dbc.transaction() as cur:
            sql = queries.GET_POINTED_FIELDS.format(model=self._model_name)
            cur.execute(sql)  # read
            for r in cur.fetch():
                yield r[0]

    def delete(self, key):
        with self._dbc.immediate_transaction() as cursor:
            key = _ensure_key(key)
            # get the record id
            r = self._get_record_by_key(key)  # read
            if r is None:
                return False
            record_id, _, _ = r
            self._delete_record(record_id)  # write
            return True

    def delete_many(self, keys):
        with self._dbc.immediate_transaction() as cursor:
            deleted_keys = list()
            for key in keys:
                if self.delete(key):
                    deleted_keys.append(key)
            return tuple(deleted_keys)

    def _get_record_by_key(self, key):
        with self._dbc.cursor() as cur:
            key_type = _get_key_type(key)
            sql = queries.GET_KV_RECORD_BY_KEY.format(key_type=key_type)
            cur.execute(sql, (key,))
            r = cur.fetchone()
            if r is None:  # nonexistent
                return
            record_id, dtype, db_timestamp = r
            return record_id, Datatype(dtype), db_timestamp

    def __getitem__(self, key):
        r = self.get(key)
        if r is None:
            raise KeyError
        return r

    def __setitem__(self, key, value):
        self.set(key, value)

    def __delitem__(self, key):
        if not self.delete(key):
            raise KeyError


def _ensure_key(key):
    if isinstance(key, int):
        return key
    if key.isnumeric():
        return int(key)
    return str(key)


def _get_key_type(key):
    if isinstance(key, str):
        return "str"
    elif isinstance(key, int):
        return "int"
    else:
        msg = "Key should be either an integer or a string."
        raise Exception(msg)


def _get_key_criteria(timestamps):
    # time_range_criteria
    if timestamps is None:
        time_range_criteria = ""
    else:
        time_range_criteria = queries.KV_CRITERIA_4.format(start=timestamps[0],
                                                         stop=timestamps[1])
    # criteria
    if time_range_criteria:
        criteria = "WHERE {}".format(time_range_criteria)
    else:
        criteria = ""
    return criteria


def _get_int_key_criteria(first, last, timestamps):
    # key_criteria
    if first is not None and last is None:
        key_criteria = queries.KV_CRITERIA_1.format(first)
    elif first is None and last is not None:
        key_criteria = queries.KV_CRITERIA_2.format(last)
    elif first is not None and last is not None:
        key_criteria = queries.KV_CRITERIA_3.format(first=first, last=last)
    else:
        key_criteria = ""
    # time_range_criteria
    if timestamps is None:
        time_range_criteria = ""
    else:
        time_range_criteria = queries.KV_CRITERIA_4.format(start=timestamps[0],
                                                         stop=timestamps[1])
    # criteria
    if key_criteria and not time_range_criteria:
        criteria = "AND {}".format(key_criteria)
    elif not key_criteria and time_range_criteria:
        criteria = "AND {}".format(time_range_criteria)
    elif key_criteria and time_range_criteria:
        criteria = "AND {} AND {}".format(key_criteria, time_range_criteria)
    else:
        criteria = ""
    return criteria


def _get_str_key_criteria(timestamps):
    # time_range_criteria
    if timestamps is None:
        time_range_criteria = ""
    else:
        time_range_criteria = queries.KV_CRITERIA_4.format(start=timestamps[0],
                                                         stop=timestamps[1])
    # criteria
    if time_range_criteria:
        criteria = "AND {}".format(time_range_criteria)
    else:
        criteria = ""
    return criteria
