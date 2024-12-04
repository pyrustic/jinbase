"""Misc functions"""
import os
import os.path
import math
from datetime import datetime, timezone
from jinbase import const


__all__ = []


def now():
    return datetime.now(timezone.utc).strftime(const.DATETIME_FORMAT)


def now_dt():
    return datetime.now(timezone.utc)


def get_timestamp(epoch_dt, dt, timestamp_precision):
    """returns milliseconds"""
    timestamp_precision = const.TimestampPrecision(timestamp_precision)
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    target_dt = dt.astimezone(tz=timezone.utc)
    epoch_dt = ensure_datetime(epoch_dt)
    t = target_dt.timestamp() - epoch_dt.timestamp()
    t = 0 if t < 0 else t
    return int(t * (10**timestamp_precision.value))


def get_datetime(epoch_dt, timestamp, timestamp_precision):
    epoch_dt = ensure_datetime(epoch_dt)
    ts = epoch_dt.timestamp() + (timestamp / (10**timestamp_precision.value))
    return datetime.fromtimestamp(ts, tz=timezone.utc)


def get_datetime_str(epoch_dt, timestamp, timestamp_precision):
    epoch_dt = ensure_datetime(epoch_dt)
    ts = epoch_dt.timestamp() + (timestamp / (10**timestamp_precision.value))
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime(const.DATETIME_FORMAT)


def ensure_datatype(value, type_ref):
    value = type_ref.adapt(value)
    if value is None:
        return
    datatype = type_ref.check(type(value))
    if datatype is None:
        raise TypeError
    return datatype


def ensure_datetime(dt):
    if isinstance(dt, str):
        # datetime.fromisoformat(dt_str) is faster than datetime.strptime(dt_str, format)
        # https://ehmatthes.com/blog/faster_than_strptime/
        # https://stackoverflow.com/questions/13468126/a-faster-strptime
        dt = datetime.fromisoformat(dt)
    return dt.astimezone(tz=timezone.utc)


def split_bin(data, chunk_size):
    if chunk_size:
        for i in range(0, len(data), chunk_size):
            yield data[i:i+chunk_size]
    else:
        yield data


def time_range_to_timestamps(epoch_dt, time_range, timestamp_precision):
    begin, end = time_range
    begin = epoch_dt if begin is None else begin
    end = now_dt() if end is None else end
    timestamp_begin = get_timestamp(epoch_dt, begin, timestamp_precision)
    timestamp_end = get_timestamp(epoch_dt, end, timestamp_precision)
    if timestamp_begin > timestamp_end:
        x = timestamp_begin
        timestamp_begin = timestamp_end
        timestamp_end = x
    return timestamp_begin, timestamp_end


def get_limit_spec(limit):
    if limit is None:
        return ""
    return "LIMIT {}".format(int(limit))


def create_backup_filename(db_filename):
    current_datetime = datetime.now()
    dt = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    basename, ext = os.path.splitext(os.path.basename(db_filename))
    return "{dt}_{basename}_backup{ext}".format(dt=dt,
                                                basename=basename,
                                                ext=ext)


def convert_size(size):
    """ Size should be in bytes.
    Return a tuple (float_or_int_val, StorageUnit instance) """
    if size == 0:
        return 0, const.StorageUnit.BYTE
    kib = 1024
    units = list(const.StorageUnit)
    i = int(math.floor(math.log(size, kib)))
    p = math.pow(kib, i)
    result = round(size/p, 2)
    if result.is_integer():
        result = int(result)
    return result, units[i]


def calc_duration(dt1, dt2=None):
    dt1 = ensure_datetime(dt1)
    dt2 = now_dt() if dt2 is None else ensure_datetime(dt2)
    time_diff = abs(dt1 - dt2)
    total_seconds = time_diff.total_seconds()
    total_minutes = total_seconds / 60
    total_hours = total_minutes / 60
    total_days = total_hours / 24
    total_weeks = total_days / 7
    if total_weeks >= 1:
        result, unit = round(total_weeks, 2), const.TimeUnit.WEEK
    elif total_days >= 1:
        result, unit = round(total_days, 2), const.TimeUnit.DAY
    elif total_hours >= 1:
        result, unit = round(total_hours, 2), const.TimeUnit.HOUR
    elif total_minutes >= 1:
        result, unit = round(total_minutes, 2), const.TimeUnit.MINUTE
    else:
        result, unit = round(total_seconds, 2), const.TimeUnit.SECOND
    if result.is_integer():
        result = int(result)
    return result, unit
