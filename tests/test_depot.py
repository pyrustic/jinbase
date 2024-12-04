import os.path
import time
import unittest
import tempfile
import paradict
from paradict import Datatype
from datetime import datetime
from jinbase import Jinbase, RecordInfo, const


USER_CARD = {"id": 42, "name": "alex", "pi": 3.14,
             "photo": b'avatar.png', "permission": None,
             "birthday": datetime(2042, 12, 25,
                                  16, 20, 59, 420),
             "books": {"sci_fi": ["Dune",
                                  "Neuromancer"],
                       "romance": ["Happy Place",
                                   "Romantic Comedy"]}}
EMPTY_USER_CARD = dict()


class TestDepotStore(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)
        self._store = self._jinbase.depot

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test_exists(self):
        rowid_1 = self._store.append("hello world")
        rowid_2 = self._store.append("hello world")
        self.assertTrue(self._store.exists(rowid_1))
        self.assertTrue(self._store.exists(rowid_2))
        self.assertFalse(self._store.exists(42))

    def test_info_method(self):
        with self.subTest("Non existent record"):
            self.assertIsNone(self._store.info(1))
        with self.subTest("Existent record"):
            rowid = self._store.append(42)
            info = self._store.info(rowid)
            self.assertIsInstance(info, RecordInfo)
            self.assertEqual(Datatype.INT, info.datatype)
            self.assertGreaterEqual(datetime.fromisoformat(self._store.now()),
                                    datetime.fromisoformat(info.created_at))

    def test_get_rowid(self):
        rowid1 = self._store.append("hello world")
        rowid2 = self._store.append("hello world")
        rowid3 = self._store.append("hello world")
        rowid4 = self._store.append("hello world")
        self.assertEqual(rowid1, self._store.uid(0))
        self.assertEqual(rowid2, self._store.uid(1))
        self.assertEqual(rowid3, self._store.uid(2))
        self.assertEqual(rowid4, self._store.uid(3))
        self.assertIsNone(self._store.uid(42))

    def test_get_position(self):
        rowid1 = self._store.append("hello world")
        rowid2 = self._store.append("hello world")
        rowid3 = self._store.append("hello world")
        rowid4 = self._store.append("hello world")
        self.assertEqual(0, self._store.position(rowid1))
        self.assertEqual(1, self._store.position(rowid2))
        self.assertEqual(2, self._store.position(rowid3))
        self.assertEqual(3, self._store.position(rowid4))
        self.assertIsNone(self._store.position(42))

    def test_count_records_method(self):
        with self.subTest("Test that new store is empty"):
            self.assertEqual(0, self._store.count_records())
        with self.subTest("Test that store contains 1 item"):
            self._store.append(USER_CARD)
            self.assertEqual(1, self._store.count_records())

    def test_count_bytes_method(self):
        size_of_user = len(paradict.pack(USER_CARD))
        # set data
        with self.subTest("Populate"):
            items = (USER_CARD, USER_CARD)
            self._store.extend(items)
        # count bytes in the store
        with self.subTest():
            r = self._store.count_bytes()
            expected = size_of_user * 2
            self.assertEqual(expected, r)
        # count bytes for a given item
        with self.subTest():
            rowid = self._store.uid(0)
            r = self._store.count_bytes(rowid)
            expected = size_of_user
            self.assertEqual(expected, r)
        # count bytes for a non-existent item
        with self.subTest():
            r = self._store.count_bytes(69)
            expected = 0
            self.assertEqual(expected, r)

    def test_is_empty(self):
        # ---
        with self.subTest("Test that new store is empty"):
            self.assertTrue(self._store.is_empty())
        # ---
        with self.subTest("Test that new store is not empty"):
            self._store.append(USER_CARD)
            self.assertFalse(self._store.is_empty())

    def test_iterate_method(self):
        self._store.append(USER_CARD)
        self._store.append(EMPTY_USER_CARD)
        expected_values = [USER_CARD, EMPTY_USER_CARD]
        returned_values = [r[1] for r in self._store.iterate()]
        self.assertEqual(expected_values, returned_values)

    def test_get_method(self):
        # test empty store
        with self.subTest("Retrieve from empty store"):
            self.assertIsNone(self._store.get(0))
        # test empty store with default value
        with self.subTest("Retrieve from empty store with default value on"):
            r = self._store.get(0, default=USER_CARD)
            self.assertEqual(USER_CARD, r)
        # Populate the store
        self._store.append(USER_CARD)
        self._store.append(EMPTY_USER_CARD)
        # positive position
        with self.subTest("Test positive positions"):
            rowid_1 = self._store.uid(0)
            rowid_2 = self._store.uid(1)
            r1 = self._store.get(rowid_1)
            r2 = self._store.get(rowid_2)
            self.assertEqual(USER_CARD, r1)
            self.assertEqual(EMPTY_USER_CARD, r2)
        # negative positions
        with self.subTest("Test negative positions"):
            rowid_1 = self._store.uid(-1)
            rowid_2 = self._store.uid(-2)
            r1 = self._store.get(rowid_1)
            r2 = self._store.get(rowid_2)
            self.assertEqual(EMPTY_USER_CARD, r1)
            self.assertEqual(USER_CARD, r2)

    def test_get_first_method(self):
        # retrieve value from empty store
        with self.subTest("Retrieve value from empty store"):
            self.assertIsNone(self._store.get_first())
        # retrieve value from empty store
        with self.subTest("Retrieve item from empty store with default value on"):
            r = self._store.get_first(default=USER_CARD)
            self.assertEqual(USER_CARD, r)
        # non-empty store
        with self.subTest("Retrieve value from non-empty store"):
            self._store.append(USER_CARD)
            self._store.append(EMPTY_USER_CARD)
        self.assertEqual(USER_CARD, self._store.get_first())

    def test_get_last_method(self):
        # retrieve value from empty store
        with self.subTest("Retrieve value from empty store"):
            self.assertIsNone(self._store.get_last())
        # retrieve value from empty store
        with self.subTest("Retrieve item from empty store with default value on"):
            r = self._store.get_last(default=USER_CARD)
            self.assertEqual(USER_CARD, r)
        # non-empty store
        with self.subTest("Retrieve value from non-empty store"):
            self._store.append(USER_CARD)
            self._store.append(EMPTY_USER_CARD)
        self.assertEqual(EMPTY_USER_CARD, self._store.get_last())

    def test_append_method(self):
        self._store.append(USER_CARD)
        rowid = self._store.uid(0)
        self.assertEqual(USER_CARD, self._store.get(rowid))

    def test_extend_method(self):
        items = [USER_CARD, USER_CARD]
        rowids = self._store.extend(items)
        self.assertEqual(USER_CARD, self._store.get(rowids[0]))
        self.assertEqual(USER_CARD, self._store.get(rowids[1]))

    def test_delete_method(self):
        items = ("Z", "A", "B", "C", "D", "E", "F")
        self._store.extend(items)
        rowid = self._store.uid(42)
        self.assertIsNone(rowid)
        r = self._store.delete(42)
        self.assertFalse(r)
        rowid = self._store.uid(-42)
        self.assertIsNone(rowid)
        self._store.delete(self._store.uid(4))  # removes "D"
        self._store.delete(self._store.uid(0))  # removes "Z"
        self._store.delete(self._store.uid(3))  # removes "E"
        self._store.delete(self._store.uid(3))  # removes "F"
        expected = ["A", "B", "C"]
        r = [x[1] for x in self._store.iterate()]
        self.assertEqual(expected, r)

    def test_delete_many_method(self):
        # append data
        rowid1 = self._store.append(USER_CARD)
        rowid2 = self._store.append(USER_CARD)
        rowid3 = self._store.append(USER_CARD)
        # delete many
        r = self._store.delete_many((rowid1, rowid2, 42))
        # test
        expected = (rowid1, rowid2)
        self.assertEqual(expected, r)
        self.assertFalse(self._store.exists(rowid1))
        self.assertFalse(self._store.exists(rowid2))
        self.assertTrue(self._store.exists(rowid3))


class TestRowidsMethod(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)
        self._store = self._jinbase.depot
        # populate the store (with numbers 10 to 20)
        self._store.append(16)
        self._store.append(11)
        self._store.append(17)
        time.sleep(0.001)  # timestamp precision matters
        self._dt1 = self._store.now_dt()
        self._store.append(12)
        self._store.append(15)
        self._store.append(20)
        self._store.append(10)
        self._store.append(19)
        self._dt2 = self._store.now_dt()
        time.sleep(0.001)  # timestamp precision matters
        self._store.append(13)
        self._store.append(14)
        self._store.append(18)
        # appended 11 items in the store

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test_rowids(self):
        expected = tuple(range(1, 12))  # 11 rowdis, from 1 to 11
        with self.subTest("Ascending"):
            r = self._store.uids()
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = self._store.uids(asc=False)
            expected = tuple(reversed(expected))
            self.assertEqual(expected, tuple(r))

    def test_rowids_with_timespan(self):
        expected = (4, 5, 6, 7, 8)
        timespan = (self._dt1, self._dt2)
        with self.subTest("Ascending"):
            r = self._store.uids(time_range=timespan)
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = self._store.uids(time_range=timespan, asc=False)
            expected = tuple(reversed(expected))
            self.assertEqual(expected, tuple(r))

    def test_rowids_with_limit(self):
        with self.subTest("Ascending"):
            r = self._store.uids(limit=3)
            expected = (1, 2, 3)
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = self._store.uids(limit=2, asc=False)
            expected =(11, 10)
            self.assertEqual(expected, tuple(r))


class TestIteration(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)
        self._store = self._jinbase.depot
        # populate the store
        self._store.append(200)
        self._store.append(30)
        time.sleep(0.001)  # timestamp precision matters
        self._dt1 = self._store.now()
        self._store.append(100)
        self._store.append(10)
        self._store.append(300)
        self._dt2 = self._store.now()
        time.sleep(0.001)  # timestamp precision matters
        self._store.append(20)

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        expected = ((1, 200),
                    (2, 30),
                    (3, 100),
                    (4, 10),
                    (5, 300),
                    (6, 20))
        with self.subTest("Ascending"):
            r = list()
            for rowid, val in self._store.iterate():
                r.append((rowid, val))
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = list()
            for rowid, val in self._store.iterate(asc=False):
                r.append((rowid, val))
            expected = tuple(reversed(expected))
            self.assertEqual(expected, tuple(r))

    def test_with_limit(self):
        with self.subTest("Ascending"):
            r = list()
            for rowid, val in self._store.iterate(limit=2):
                r.append((rowid, val))
            expected = ((1, 200),
                        (2, 30))
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = list()
            for rowid, val in self._store.iterate(limit=2, asc=False):
                r.append((rowid, val))
            expected = ((6, 20),
                        (5, 300))
            self.assertEqual(expected, tuple(r))

    def test_with_timespan(self):
        expected = ((3, 100),
                    (4, 10),
                    (5, 300))
        timespan = (self._dt1, self._dt2)
        with self.subTest("Ascending"):
            r = list()
            for rowid, val in self._store.iterate(time_range=timespan):
                r.append((rowid, val))
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = list()
            for rowid, val in self._store.iterate(time_range=timespan, asc=False):
                r.append((rowid, val))
            expected = tuple(reversed(expected))
            self.assertEqual(expected, tuple(r))


class TestSmallestChunkSize(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        smallest_chunk_size = 1  # 1 byte
        self._jinbase = Jinbase(self._filename,
                                chunk_size=smallest_chunk_size)
        self._store = self._jinbase.depot

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):  # ensure that the db works fine with smallest chunk_size
        # append data
        with self.subTest("Append complex data"):
            rowid = self._store.append(USER_CARD)
            r = self._store.get(rowid)
            self.assertEqual(USER_CARD, r)
        # append empty dict
        with self.subTest("Append empty dict as value"):
            rowid = self._store.append(EMPTY_USER_CARD)
            r = self._store.get(rowid)
            self.assertEqual(EMPTY_USER_CARD, r)
        # append empty bytes
        with self.subTest("Append empty byte as value"):
            rowid = self._store.append(b'')
            r = self._store.get(rowid)
            self.assertEqual(b'', r)
        # append string
        with self.subTest("Append string as value"):
            rowid = self._store.append("alex")
            r = self._store.get(rowid)
            self.assertEqual("alex", r)
        # Try to append None as value
        with self.subTest("Try to append None as value"):
            rowid = self._store.append(None)
            self.assertIsNone(rowid)

    def test_count_chunks(self):
        rowid1 = self._store.append(USER_CARD)
        rowid2 = self._store.append(USER_CARD)
        rowid2 = self._store.append(USER_CARD)
        size_user_card = len(paradict.pack(USER_CARD))  # n bytes
        # count total chunks
        with self.subTest("Count total chunks"):
            n_chunks = self._store.count_chunks()
            expected_n_chunks = size_user_card * 3
            self.assertEqual(expected_n_chunks, n_chunks)
        # count user1 chunks
        with self.subTest("Count first item chunks"):
            n_chunks = self._store.count_chunks(rowid1)
            expected_n_chunks = size_user_card
            self.assertEqual(expected_n_chunks, n_chunks)
        # remove first item and count total chunks
        with self.subTest("Remove first item and count total chunks"):
            self._store.delete(rowid1)
            n_chunks = self._store.count_chunks()
            expected_n_chunks = size_user_card * 2
            self.assertEqual(expected_n_chunks, n_chunks)


class TestDefaultValue(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        smallest_chunk_size = 1  # 1 byte
        self._jinbase = Jinbase(self._filename,
                                chunk_size=smallest_chunk_size)
        self._store = self._jinbase.depot

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        self.assertEqual(USER_CARD, self._store.get(42, default=USER_CARD))
        self.assertEqual(USER_CARD, self._store.get_first(default=USER_CARD))
        self.assertEqual(USER_CARD, self._store.get_last(default=USER_CARD))


class TestTransactionContext(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)
        self._store = self._jinbase.depot

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        with self._store.transaction():  # TransactionMode.IMMEDIATE by default
            rowid = self._store.append(USER_CARD)
            self._store.append(USER_CARD)
            self._store.delete(rowid)


class TestLargeBinaryData(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)
        self._store = self._jinbase.depot

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        data = b'\x00' * (const.CHUNK_SIZE * 2)
        rowid = self._store.append(data)
        self.assertEqual(data, self._store.get(rowid))


class TestBlobAccess(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        smallest_chunk_size = 1  # 1 byte
        self._jinbase = Jinbase(self._filename,
                                chunk_size=smallest_chunk_size)
        self._store = self._jinbase.depot
        self._data = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self._rowid = self._store.append(self._data)

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test_read_method(self):
        with self._store.open_blob(self._rowid) as blob:
            with self.subTest():
                r = blob.read(0)
                expected = b''
                self.assertEqual(expected, r)
            with self.subTest():
                r = blob.read(1)
                expected = self._data[0:1]
                self.assertEqual(expected, r)
            with self.subTest():
                r = blob.read(1)
                expected = self._data[1:2]
                self.assertEqual(expected, r)
            with self.subTest():
                r = blob.read(2)
                expected = self._data[2:4]
                self.assertEqual(expected, r)

    def test_auto_full_read(self):
        with self._store.open_blob(self._rowid) as blob:
            with self.subTest():
                r = blob.read()
                expected = self._data
                self.assertEqual(expected, r)
            with self.subTest():
                r = blob.read()
                expected = b''
                self.assertEqual(expected, r)

    def test_manual_full_read(self):
        with self._store.open_blob(self._rowid) as blob:
            with self.subTest():
                n = len(self._data)
                r = blob.read(n)
                expected = self._data
                self.assertEqual(expected, r)
            with self.subTest():
                r = blob.read()
                expected = b''
                self.assertEqual(expected, r)

    def test_alternative_read(self):
        with self._store.open_blob(self._rowid) as blob:
            with self.subTest():
                r = blob[0]
                expected = self._data[0:1]
                self.assertEqual(expected, r)
            with self.subTest():
                r = blob[0]
                expected = self._data[0:1]
                self.assertEqual(expected, r)
            with self.subTest():
                r = blob[0:]
                expected = self._data
                self.assertEqual(expected, r)
            with self.subTest():
                r = blob[0:]
                expected = self._data
                self.assertEqual(expected, r)
            with self.subTest():
                r = blob[0:len(self._data)]
                expected = self._data
                self.assertEqual(expected, r)
            with self.subTest():
                r = blob[-1]
                expected = b'Z'
                self.assertEqual(expected, r)
            with self.subTest():
                r = blob[-2]
                expected = b'Y'
                self.assertEqual(expected, r)

    def test_seek_and_tell(self):
        with self._store.open_blob(self._rowid) as blob:
            with self.subTest():
                r = blob.tell()
                expected = 0
                self.assertEqual(expected, r)
            with self.subTest():
                blob.read(2)
                r = blob.tell()
                expected = 2
                self.assertEqual(expected, r)
            with self.subTest():
                blob.seek(0)
                r = blob.tell()
                expected = 0
                self.assertEqual(expected, r)
            with self.subTest():
                r = blob.read()
                expected = self._data
                self.assertEqual(expected, r)
                r = blob.tell()
                expected = len(self._data)
                self.assertEqual(expected, r)
            with self.subTest():
                blob.seek(0, os.SEEK_END)
                r = blob.read()
                expected = b''
                self.assertEqual(expected, r)
                r = blob.tell()
                expected = len(self._data)
                self.assertEqual(expected, r)

    def test_forbidden_operations(self):
        with self._store.open_blob(self._rowid) as blob:
            with self.assertRaises(NotImplementedError):
                blob.write(b'')
            with self.assertRaises(NotImplementedError):
                blob[0] = b''
            with self.assertRaises(ValueError):
                forbidden_step_value = 2  # only 1 as step value is allowed !
                blob[slice(0, 1, forbidden_step_value)]


class TestFields(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)
        self._store = self._jinbase.depot

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test_fields_method(self):
        with self.subTest():
            uid_1 = self._store.append(["alex", 42])
            r = tuple(self._store.fields())
            self.assertEqual(tuple(), r)
        with self.subTest():
            uid_2 = self._store.append({"name": "alex", "id": 42, 1: 1})
            r = tuple(self._store.fields())
            expected = ("id", "name")
            self.assertEqual(expected, r)
        with self.subTest():
            self._store.delete(uid_2)
            r = tuple(self._store.fields())
            self.assertEqual(tuple(), r)

    def test_load_field_method(self):
        with self.subTest():
            uid = self._store.append(USER_CARD)
            r = self._store.load_field(uid, "birthday")
            expected = USER_CARD["birthday"]
            self.assertEqual(expected, r)
        with self.subTest():
            r = self._store.load_field(uid, "nonexistent-field")
            self.assertIsNone(r)
        with self.subTest():
            r = self._store.load_field(uid, "permission")
            expected = USER_CARD["permission"]
            self.assertEqual(expected, r)

    def test_load_field_method_with_custom_default_value(self):
        with self.subTest():
            uid = self._store.append(USER_CARD)
            r = self._store.load_field(uid, "birthday",
                                       default=-1)
            expected = USER_CARD["birthday"]
            self.assertEqual(expected, r)
        with self.subTest():
            r = self._store.load_field(uid, "nonexistent-field",
                                       default=-1)
            self.assertEqual(-1, r)
        with self.subTest():
            r = self._store.load_field(uid, "permission",
                                       default=-1)
            expected = USER_CARD["permission"]
            self.assertEqual(expected, r)


if __name__ == "__main__":
    unittest.main()
