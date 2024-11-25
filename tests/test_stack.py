import os.path
import unittest
import tempfile
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


class TestStackStore(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)
        self._store = self._jinbase.stack

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test_info_top_method(self):
        with self.subTest("Non existent record"):
            self.assertIsNone(self._store.info_top())
        self._store.push("hello world")
        self._store.push(USER_CARD)
        with self.subTest("Existent record"):
            info = self._store.info_top()
            self.assertIsInstance(info, RecordInfo)
            self.assertEqual(Datatype.DICT, info.datatype)
            self.assertGreaterEqual(datetime.fromisoformat(self._store.now()),
                                    datetime.fromisoformat(info.created_at))

    def test_count_records_method(self):
        with self.subTest("Test that new store is empty"):
            self.assertEqual(0, self._store.count_records())
        with self.subTest("Test that store contains 1 item"):
            self._store.push(USER_CARD)
            self.assertEqual(1, self._store.count_records())

    def test_count_bytes_method(self):
        size_of_user = len(paradict.pack(USER_CARD))
        # set data
        self._store.push(USER_CARD)
        self._store.push(USER_CARD)
        # count bytes in the store
        with self.subTest():
            r = self._store.count_bytes()
            expected = size_of_user * 2
            self.assertEqual(expected, r)

    def test_count_top_bytes_method(self):
        size_of_user = len(paradict.pack(USER_CARD))
        # set data
        self._store.push(USER_CARD)
        self._store.push(USER_CARD)
        # count bytes of the item on top
        with self.subTest():
            r = self._store.count_top_bytes()
            expected = size_of_user
            self.assertEqual(expected, r)

    def test_is_empty(self):
        # ---
        with self.subTest("Test that new store is empty"):
            self.assertTrue(self._store.is_empty())
        # ---
        with self.subTest("Test that new store is not empty"):
            self._store.push(USER_CARD)
            self.assertFalse(self._store.is_empty())

    def test_push_method(self):
        with self.subTest("Test empty stack store"):
            self.assertEqual(0, self._store.count_records())
        with self.subTest("Test stack store after populating it"):
            self._store.push(USER_CARD)
            self.assertEqual(1, self._store.count_records())
            self._store.push(EMPTY_USER_CARD)
            self.assertEqual(2, self._store.count_records())

    def test_push_many_method(self):
        r = self._store.push_many((10, 11, 12, 13))
        expected = (1, 2, 3, 4)
        self.assertEqual(expected, r)
        self.assertEqual(4, self._store.count_records())

    def test_pop_method(self):
        with self.subTest("Test empty stack store"):
            self.assertIsNone(self._store.pop())
        with self.subTest("Test empty stack store with default value on"):
            self.assertEqual(USER_CARD, self._store.pop(default=USER_CARD))
        with self.subTest("Test stack store after populating it"):
            self._store.push(EMPTY_USER_CARD)
            self._store.push(USER_CARD)
            self.assertEqual(2, self._store.count_records())
            self.assertEqual(USER_CARD, self._store.pop())
            self.assertEqual(1, self._store.count_records())
            self.assertEqual(EMPTY_USER_CARD, self._store.pop())
            self.assertEqual(0, self._store.count_records())

    def test_peek_method(self):
        with self.subTest("Test empty stack store"):
            self.assertIsNone(self._store.peek())
        with self.subTest("Test empty stack store with default value on"):
            self.assertEqual(USER_CARD, self._store.peek(default=USER_CARD))
        with self.subTest("Test stack store after populating it"):
            self._store.push(EMPTY_USER_CARD)
            self._store.push(USER_CARD)
            self.assertEqual(USER_CARD, self._store.peek())
            self._store.pop()
            self.assertEqual(EMPTY_USER_CARD, self._store.peek())

    def test_get_top_rowid(self):
        rowid1 = self._store.push(USER_CARD)
        rowid2 = self._store.push(USER_CARD)
        self.assertEqual(rowid2, self._store.top_uid())


class TestSmallestChunkSize(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        smallest_chunk_size = 1
        self._jinbase = Jinbase(self._filename,
                                chunk_size=smallest_chunk_size)
        self._store = self._jinbase.stack

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        with self.subTest("Test empty stack store"):
            self.assertEqual(0, self._store.count_records())
        with self.subTest("Test stack store after populating it"):
            self._store.push(USER_CARD)
            self.assertEqual(1, self._store.count_records())
            self._store.push(EMPTY_USER_CARD)
            self.assertEqual(2, self._store.count_records())
        with self.subTest("Test pop"):
            r = self._store.pop()
            self.assertEqual(EMPTY_USER_CARD, r)
            self.assertEqual(1, self._store.count_records())
            r = self._store.pop()
            self.assertEqual(USER_CARD, r)
            self.assertEqual(0, self._store.count_records())

    def test_count_top_chunks_method(self):
        self._store.push(EMPTY_USER_CARD)
        self._store.push(USER_CARD)
        size_user_card = len(paradict.pack(USER_CARD))  # n bytes
        size_empty_user_card = len(paradict.pack(EMPTY_USER_CARD))  # n bytes
        # count total chunks
        with self.subTest("Count total chunks"):
            n_chunks = self._store.count_chunks()
            expected_n_chunks = size_user_card + size_empty_user_card
            self.assertEqual(expected_n_chunks, n_chunks)
        # count front chunks
        with self.subTest("Count chunks at top"):
            n_chunks = self._store.count_top_chunks()
            expected_n_chunks = size_user_card
            self.assertEqual(expected_n_chunks, n_chunks)
        # pop then count total chunks
        with self.subTest("Pop then count total chunks"):
            self._store.pop()
            n_chunks = self._store.count_chunks()
            expected_n_chunks = size_empty_user_card
            self.assertEqual(expected_n_chunks, n_chunks)


class TestDefaultValue(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        smallest_chunk_size = 1  # 1 byte
        self._jinbase = Jinbase(self._filename,
                                chunk_size=smallest_chunk_size)
        self._store = self._jinbase.stack

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        self.assertEqual(USER_CARD, self._store.pop(default=USER_CARD))
        self.assertEqual(USER_CARD, self._store.peek(default=USER_CARD))


class TestTransactionContext(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)
        self._store = self._jinbase.stack

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        with self._store.transaction():  # TransactionMode.IMMEDIATE by default
            self._store.push(USER_CARD)
            self._store.push(USER_CARD)
            self._store.pop()


class TestLargeBinaryData(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)
        self._store = self._jinbase.stack

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        data = b'\x00' * (const.CHUNK_SIZE * 2)
        self._store.push(data)
        self.assertEqual(data, self._store.pop())


if __name__ == "__main__":
    unittest.main()
