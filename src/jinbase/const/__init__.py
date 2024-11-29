"""Project-wide constants are defined in this module."""
import os.path
from enum import Enum, unique

__all__ = ["Model", "TimestampPrecision",
           "TimeUnit", "StorageUnit", "CHUNK_SIZE", "JINBASE_HOME",
           "JINBASE_VERSION", "USER_HOME", "DATETIME_FORMAT",
           "TIMESTAMP_PRECISION", "TIMEOUT"]


# models (key-value, depot, queue, and stack)
@unique
class Model(Enum):
    KV = 1
    DEPOT = 2
    QUEUE = 3
    STACK = 4


@unique
class TimestampPrecision(Enum):
    SECONDS = 0
    MILLISECONDS = 3
    MICROSECONDS = 6
    NANOSECONDS = 9


@unique
class StorageUnit(Enum):
    BYTE = "B"
    KIBIBYTE = "KiB"
    MEBIBYTE = "MiB"
    GIBIBYTE = "GiB"
    TEBIBYTE = "TiB"


@unique
class TimeUnit(Enum):
    SECOND = "sec"
    MINUTE = "min"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"


# Default timestamp precision
TIMESTAMP_PRECISION = TimestampPrecision.MILLISECONDS


# directories
USER_HOME = os.path.expanduser("~")
JINBASE_HOME = os.path.join(USER_HOME, "JinbaseHome")

# chunk size
CHUNK_SIZE = 2**20  # 1 MiB

# timeout
TIMEOUT = 5.0

# version
JINBASE_VERSION = 1

# datetime string
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%fZ"
