import os
import os.path
import unittest
import tempfile
import time
import paradict
from datetime import datetime
from paradict import Datatype
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


class TestKvStore(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)
        self._store = self._jinbase.kv

    def tearDown(self):
        self._jinbase.close()
        # the Try/Except is needed here because I can only
        # benefit from the constructor's "ignore_cleanup_errors=True"
        # in Python 3.10
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test_info_method(self):
        with self.subTest("Non existent record"):
            self.assertIsNone(self._store.info("user1"))
        with self.subTest("Existent record"):
            self._store.set("user1", 42)
            info = self._store.info("user1")
            self.assertIsInstance(info, RecordInfo)
            self.assertEqual(Datatype.INT, info.datatype)
            self.assertGreaterEqual(datetime.fromisoformat(self._store.now()),
                                    datetime.fromisoformat(info.created_at))

    def test_count_records_method(self):
        # Test that new store is empty
        with self.subTest("Test that new store is empty"):
            self.assertEqual(0, self._store.count_records())
        # Test that store contains 1 item
        with self.subTest("Test that store contains 1 item"):
            self._store.set("user", USER_CARD)
            self.assertEqual(1, self._store.count_records())

    def test_count_bytes_method(self):
        size_of_user = len(paradict.pack(USER_CARD))
        # Set data
        with self.subTest("Set data"):
            self._store.set("user1", USER_CARD)
            self._store.set("user2", USER_CARD)
        # Count bytes in the store
        with self.subTest("Count bytes in the store"):
            r = self._store.count_bytes()
            expected = size_of_user * 2
            self.assertEqual(expected, r)
        # Get the size of the value of an item
        with self.subTest("Get the size of the value of an item"):
            r = self._store.count_bytes("user1")
            expected = size_of_user
            self.assertEqual(expected, r)
        # Get the size of the value of a non-existent item
        with self.subTest("Get the size of the value of a non-existent item"):
            r = self._store.count_bytes("fake-key")
            expected = 0
            self.assertEqual(expected, r)

    def test_is_empty(self):
        # ---
        with self.subTest("Test that new store is empty"):
            self.assertTrue(self._store.is_empty())
        # ---
        with self.subTest("Test that new store is not empty"):
            self._store.set("user", USER_CARD)
            self.assertFalse(self._store.is_empty())

    def test_get_method(self):
        self._store.set("user", USER_CARD)
        with self.subTest("Retrieve a registered key"):
            r = self._store.get("user")
            self.assertEqual(USER_CARD, r)
        with self.subTest("Retrieve a registered key with default value on"):
            r = self._store.get("user", default=EMPTY_USER_CARD)
            self.assertEqual(USER_CARD, r)
        with self.subTest("Retrieve an unregistered key"):
            r = self._store.get("unregistered-user")
            self.assertIsNone(r)
        with self.subTest("Retrieve an unregistered key with default value on"):
            r = self._store.get("unregistered-user", default=EMPTY_USER_CARD)
            self.assertEqual(EMPTY_USER_CARD, r)

    def test_set_method(self):
        # set data
        with self.subTest("Set complex data"):
            rowid = self._store.set("user", USER_CARD)
            self.assertEqual(1, rowid)
            r = self._store.get("user")
            self.assertEqual(USER_CARD, r)
            self.assertEqual(1, self._store.count_chunks())
            self.assertEqual(1, self._store.count_chunks("user"))
        # set empty dict
        with self.subTest("Set empty dict as value"):
            self._store.set("user", EMPTY_USER_CARD)
            r = self._store.get("user")
            self.assertEqual(EMPTY_USER_CARD, r)
        # set empty bytes
        with self.subTest("Set empty byte as value"):
            self._store.set("user", b'')
            r = self._store.get("user")
            self.assertEqual(b'', r)
        # set string
        with self.subTest("Set string as value"):
            self._store.set("user", "alex")
            r = self._store.get("user")
            self.assertEqual("alex", r)
        # set None as value
        with self.subTest("Set None as value"):
            rowid = self._store.set("user", None)
            self.assertIsNone(rowid)
            r = self._store.get("user")
            self.assertIsNotNone(r)

    def test_replace_method(self):
        # replace data that doesnt exist
        with self.subTest("Set complex data"):
            r = self._store.replace("user", USER_CARD)
            self.assertIsNone(r)
            r = self._store.exists("user")
            self.assertFalse(r)
        # replace data that does exist
        with self.subTest("Set complex data"):
            self._store.set("user", USER_CARD)
            r = self._store.replace("user", EMPTY_USER_CARD)
            self.assertEqual(USER_CARD, r)
            r = self._store.get("user")
            self.assertEqual(EMPTY_USER_CARD, r)

    def test_exists_method(self):
        self._store.set("user1", EMPTY_USER_CARD)
        with self.subTest("Registered key"):
            r = self._store.exists("user1")
            self.assertTrue(r)
        with self.subTest("Unregistered key"):
            r = self._store.exists("user2")
            self.assertFalse(r)

    def test_update_method(self):
        dict_data = {"user1": USER_CARD, "user2": EMPTY_USER_CARD}
        rowid = self._store.set("user", USER_CARD)
        rowids = self._store.update(dict_data)
        self.assertEqual(1, rowid)
        self.assertEqual({"user1": 2, "user2": 3}, rowids)
        expected_keys = ("user", "user1", "user2")
        self.assertEqual(expected_keys, tuple(self._store.keys()))

    def test_get_rowid(self):
        rowid1 = self._store.set("k1", "hello world")
        rowid2 = self._store.set("k2", "hello world")
        rowid3 = self._store.set(1, "hello world")
        rowid4 = self._store.set(2, "hello world")
        self.assertEqual(rowid1, self._store.uid("k1"))
        self.assertEqual(rowid2, self._store.uid("k2"))
        self.assertEqual(rowid3, self._store.uid(1))
        self.assertEqual(rowid4, self._store.uid(2))
        self.assertIsNone(self._store.uid(3))

    def test_get_key(self):
        key1, key2, key3, key4 = "k1", "k2", 1, 2
        rowid1 = self._store.set(key1, "hello world")
        rowid2 = self._store.set(key2, "hello world")
        rowid3 = self._store.set(key3, "hello world")
        rowid4 = self._store.set(key4, "hello world")
        self.assertEqual(key1, self._store.key(rowid1))
        self.assertEqual(key2, self._store.key(rowid2))
        self.assertEqual(key3, self._store.key(rowid3))
        self.assertEqual(key4, self._store.key(rowid4))
        self.assertIsNone(self._store.key(42))

    def test_list_keys_method(self):
        # Case 1: No keys
        with self.subTest():
            r = self._store.keys()
            self.assertEqual(tuple(), tuple(r))
        # Case 2: Two registered keys
        with self.subTest():
            self._store.set("user1", EMPTY_USER_CARD)
            self._store.set("user2", EMPTY_USER_CARD)
            r = self._store.keys()
            expected = ("user1", "user2")
            self.assertEqual(expected, tuple(r))

    def test_delete_method(self):
        # set data
        with self.subTest("Set data"):
            self._store.set("user", USER_CARD)
            r = self._store.get("user")
            self.assertEqual(USER_CARD, r)
        with self.subTest("Remove data"):
            self._store.delete("user")
            r = self._store.get("user")
            self.assertIsNone(r)

    def test_delete_many_method(self):
        # set data
        self._store.set("user1", USER_CARD)
        self._store.set("user2", USER_CARD)
        self._store.set("user3", USER_CARD)
        # delete many
        r = self._store.delete_many(("user1", "user2", "user42"))
        # test
        expected = ("user1", "user2")
        self.assertEqual(expected, r)
        self.assertFalse(self._store.exists("user1"))
        self.assertFalse(self._store.exists("user2"))
        self.assertTrue(self._store.exists("user3"))

    def test_delete_all_method(self):
        self._store.set("user1", USER_CARD)
        self._store.set("user2", USER_CARD)
        self._store.set("user3", USER_CARD)
        self._store.delete_all()
        r = self._store.get("user")
        self.assertIsNone(r)

    def test_alternative_get_set(self):
        with self.assertRaises(KeyError):
            self._store["user"]
        self._store["user"] = USER_CARD
        r = self._store["user"]
        self.assertEqual(USER_CARD, r)

    def test_alternative_delete(self):
        with self.assertRaises(KeyError):
            del self._store["user"]
        self._store["user"] = USER_CARD
        del self._store["user"]
        with self.assertRaises(KeyError):
            self._store["user"]


class TestKeysMethod(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)
        self._store = self._jinbase.kv
        # populate the store
        self._store.set("user3", EMPTY_USER_CARD)
        self._store.set(4, EMPTY_USER_CARD)
        self._store.set("user2", EMPTY_USER_CARD)
        time.sleep(0.001)  # timestamp precision matters
        self._dt1 = self._store.now_dt()
        self._store.set(2, EMPTY_USER_CARD)
        self._store.set("admin2", EMPTY_USER_CARD)
        self._store.set(1, EMPTY_USER_CARD)
        self._store.set("user1", EMPTY_USER_CARD)
        self._store.set(3, EMPTY_USER_CARD)
        self._dt2 = self._store.now_dt()
        time.sleep(0.001)  # timestamp precision matters
        self._store.set("admin1", EMPTY_USER_CARD)
        self._store.set(5, EMPTY_USER_CARD)
        self._store.set("admin3", EMPTY_USER_CARD)

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test_keys(self):
        expected = (1, 2, 3, 4, 5,
                    "admin1", "admin2", "admin3",
                    "user1", "user2", "user3")
        with self.subTest("Ascending"):
            r = self._store.keys()
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = self._store.keys(asc=False)
            expected = tuple(reversed(expected))
            self.assertEqual(expected, tuple(r))

    def test_keys_with_timespan(self):
        expected = (1, 2, 3, "admin2", "user1")
        timespan = (self._dt1, self._dt2)
        with self.subTest("Ascending"):
            r = self._store.keys(time_range=timespan)
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = self._store.keys(time_range=timespan, asc=False)
            expected = tuple(reversed(expected))
            self.assertEqual(expected, tuple(r))

    def test_keys_with_limit(self):
        with self.subTest("Ascending"):
            r = self._store.keys(limit=3)
            expected = (1, 2, 3)
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = self._store.keys(limit=2, asc=False)
            expected =("user3", "user2")
            self.assertEqual(expected, tuple(r))

    def test_str_key(self):
        expected = ("admin1", "admin2", "admin3",
                    "user1", "user2", "user3")
        with self.subTest("Ascending"):
            r = self._store.str_keys()
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = self._store.str_keys(asc=False)
            expected = tuple(reversed(expected))
            self.assertEqual(expected, tuple(r))

    def test_str_key_with_timespan(self):
        expected = ("admin2", "user1")
        timespan = (self._dt1, self._dt2)
        with self.subTest("Ascending"):
            r = self._store.str_keys(time_range=timespan)
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = self._store.str_keys(time_range=timespan, asc=False)
            expected = tuple(reversed(expected))
            self.assertEqual(expected, tuple(r))

    def test_str_key_with_glob(self):
        expected = ("admin1", "admin2", "admin3")
        with self.subTest("Ascending"):
            r = self._store.str_keys("admin*")
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = self._store.str_keys("admin*", asc=False)
            expected = tuple(reversed(expected))
            self.assertEqual(expected, tuple(r))

    def test_str_key_with_limit(self):
        expected = ("admin1", "admin2")
        with self.subTest("Ascending"):
            r = self._store.str_keys(limit=2)
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = self._store.str_keys(limit=2, asc=False)
            expected = ("user3", "user2")
            self.assertEqual(expected, tuple(r))

    def test_int_key(self):
        expected = (1, 2, 3, 4, 5)
        with self.subTest("Ascending"):
            r = self._store.int_keys()
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = self._store.int_keys(asc=False)
            expected = tuple(reversed(expected))
            self.assertEqual(expected, tuple(r))

    def test_int_key_with_timespan(self):
        expected = (1, 2, 3)
        timespan = (self._dt1, self._dt2)
        with self.subTest("Ascending"):
            r = self._store.int_keys(time_range=timespan)
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = self._store.int_keys(time_range=timespan, asc=False)
            expected = tuple(reversed(expected))
            self.assertEqual(expected, tuple(r))

    def test_int_key_with_interval(self):
        expected = (2, 3, 4)
        with self.subTest("Ascending"):
            r = self._store.int_keys(2, 4)
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = self._store.int_keys(2, 4, asc=False)
            expected = tuple(reversed(expected))
            self.assertEqual(expected, tuple(r))

    def test_int_key_with_limit(self):
        expected = (1, 2)
        with self.subTest("Ascending"):
            r = self._store.int_keys(limit=2)
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = self._store.int_keys(limit=2, asc=False)
            expected = (5, 4)
            self.assertEqual(expected, tuple(r))


class TestIteration(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)
        self._store = self._jinbase.kv
        # populate the store
        self._store.set("user2", 200)
        self._store.set(3, 30)
        time.sleep(0.001)  # timestamp precision matters
        self._dt1 = self._store.now()
        self._store.set("user1", 100)
        self._store.set(1, 10)
        self._store.set("user3", 300)
        self._dt2 = self._store.now()
        time.sleep(0.001)  # timestamp precision matters
        self._store.set(2, 20)

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        expected = ((1, 10),
                    (2, 20),
                    (3, 30),
                    ("user1", 100),
                    ("user2", 200),
                    ("user3", 300))
        with self.subTest("Ascending"):
            r = list()
            for key, val in self._store.iterate():
                r.append((key, val))
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = list()
            for key, val in self._store.iterate(asc=False):
                r.append((key, val))
            expected = tuple(reversed(expected))
            self.assertEqual(expected, tuple(r))

    def test_with_limit(self):
        with self.subTest("Ascending"):
            r = list()
            for key, val in self._store.iterate(limit=2):
                r.append((key, val))
            expected = ((1, 10),
                        (2, 20))
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = list()
            for key, val in self._store.iterate(limit=2, asc=False):
                r.append((key, val))
            expected = (("user3", 300),
                        ("user2", 200))
            self.assertEqual(expected, tuple(r))

    def test_with_timespan(self):
        expected = ((1, 10),
                    ("user1", 100),
                    ("user3", 300))
        timespan = (self._dt1, self._dt2)
        with self.subTest("Ascending"):
            r = list()
            for key, val in self._store.iterate(time_range=timespan):
                r.append((key, val))
            self.assertEqual(expected, tuple(r))
        with self.subTest("Descending"):
            r = list()
            for key, val in self._store.iterate(time_range=timespan, asc=False):
                r.append((key, val))
            expected = tuple(reversed(expected))
            self.assertEqual(expected, tuple(r))


class TestSmallestChunkSize(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        smallest_chunk_size = 1  # 1 byte
        self._jinbase = Jinbase(self._filename,
                                chunk_size=smallest_chunk_size)
        self._store = self._jinbase.kv

    def tearDown(self):
        self._jinbase.close()
        # the Try/Except is needed here because I can only
        # benefit from the constructor's "ignore_cleanup_errors=True"
        # in Python 3.10
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):  # ensure that the db works fine with smallest chunk_size
        # set data
        with self.subTest("Set complex data"):
            self._store.set("user", USER_CARD)
            r = self._store.get("user")
            self.assertEqual(USER_CARD, r)
        # set empty dict
        with self.subTest("Set empty dict as value"):
            self._store.set("user", EMPTY_USER_CARD)
            r = self._store.get("user")
            self.assertEqual(EMPTY_USER_CARD, r)
        # set empty bytes
        with self.subTest("Set empty byte as value"):
            self._store.set("user", b'')
            r = self._store.get("user")
            self.assertEqual(b'', r)
        # set string
        with self.subTest("Set string as value"):
            self._store.set("user", "alex")
            r = self._store.get("user")
            self.assertEqual("alex", r)
        # set None as value
        with self.subTest("Set None as value"):
            x = self._store.set("user", None)
            self.assertFalse(x)
            r = self._store.get("user")
            self.assertIsNotNone(r)

    def test_count_chunks(self):
        self._store.set("user1", USER_CARD)
        self._store.set("user2", USER_CARD)
        self._store.set("user3", USER_CARD)
        size_user_card = len(paradict.pack(USER_CARD))  # n bytes
        # count total chunks
        with self.subTest("Count total chunks"):
            n_chunks = self._store.count_chunks()
            expected_n_chunks = size_user_card * 3
            self.assertEqual(expected_n_chunks, n_chunks)
        # count user1 chunks
        with self.subTest("Count user1 chunks"):
            n_chunks = self._store.count_chunks("user1")
            expected_n_chunks = size_user_card
            self.assertEqual(expected_n_chunks, n_chunks)
        # remove user3 and count total chunks
        with self.subTest("Remove user3 and count total chunks"):
            self._store.delete("user3")
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
        self._store = self._jinbase.kv

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        self.assertEqual(USER_CARD, self._store.get(42, default=USER_CARD))


class TestTransactionContext(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)
        self._store = self._jinbase.kv

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        with self._store.transaction():  # TransactionMode.IMMEDIATE by default
            self._store.set("user1", USER_CARD)
            self._store.set("user2", USER_CARD)
            self._store.delete("user1")


class TestLargeBinaryData(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)
        self._store = self._jinbase.kv

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        data = b'\x00' * (const.CHUNK_SIZE * 2)
        self._store.set("user", data)
        self.assertEqual(data, self._store.get("user"))


class TestBlobAccess(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        smallest_chunk_size = 1  # 1 byte
        self._jinbase = Jinbase(self._filename, chunk_size=smallest_chunk_size)
        self._store = self._jinbase.kv
        self._data = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self._store.set("key", self._data)

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test_read_method(self):
        with self._store.open_blob("key") as blob:
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
        with self._store.open_blob("key") as blob:
            with self.subTest():
                r = blob.read()
                expected = self._data
                self.assertEqual(expected, r)
            with self.subTest():
                r = blob.read()
                expected = b''
                self.assertEqual(expected, r)

    def test_manual_full_read(self):
        with self._store.open_blob("key") as blob:
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
        with self._store.open_blob("key") as blob:
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
        with self._store.open_blob("key") as blob:
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
        with self._store.open_blob("key") as blob:
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
        self._store = self._jinbase.kv

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test_fields_method(self):
        with self.subTest():
            self._store.set("user1", ["alex", 42])
            r = tuple(self._store.fields())
            self.assertEqual(tuple(), r)
        with self.subTest():
            self._store.set("user2", {"name": "alex", "id": 42, 1: 1})
            r = tuple(self._store.fields())
            expected = ("id", "name")
            self.assertEqual(expected, r)
        with self.subTest():
            self._store.delete("user2")
            r = tuple(self._store.fields())
            self.assertEqual(tuple(), r)

    def test_load_field_method(self):
        with self.subTest():
            self._store.set("user", USER_CARD)
            r = self._store.load_field("user", "birthday")
            expected = USER_CARD["birthday"]
            self.assertEqual(expected, r)
        with self.subTest():
            r = self._store.load_field("user", "nonexistent-field")
            self.assertIsNone(r)
        with self.subTest():
            r = self._store.load_field("user", "permission")
            expected = USER_CARD["permission"]
            self.assertEqual(expected, r)

    def test_load_field_method_with_custom_default_value(self):
        with self.subTest():
            self._store.set("user", USER_CARD)
            r = self._store.load_field("user", "birthday",
                                       default=-1)
            expected = USER_CARD["birthday"]
            self.assertEqual(expected, r)
        with self.subTest():
            r = self._store.load_field("user", "nonexistent-field",
                                       default=-1)
            self.assertEqual(-1, r)
        with self.subTest():
            r = self._store.load_field("user", "permission",
                                       default=-1)
            expected = USER_CARD["permission"]
            self.assertEqual(expected, r)


if __name__ == "__main__":
    unittest.main()
