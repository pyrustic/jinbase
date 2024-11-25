import unittest


class TestImports(unittest.TestCase):

    def test_import_classes(self):
        try:
            # import classes
            from jinbase import Jinbase
            from jinbase import TypeRef
            # import enums
            from jinbase import Model
            from jinbase import TimestampPrecision
            # import namedtuple
            from jinbase import RecordInfo
            # import consts
            from jinbase import TIMEOUT
            from jinbase import CHUNK_SIZE
            from jinbase import TIMESTAMP_PRECISION
            from jinbase import DATETIME_FORMAT
            from jinbase import USER_HOME
            from jinbase import JINBASE_HOME
            from jinbase import JINBASE_VERSION
        except ImportError:
            self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
