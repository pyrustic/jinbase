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


class TestQueueStore(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)
        self._store = self._jinbase.queue

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test_info_front_method(self):
        with self.subTest("Non existent record"):
            self.assertIsNone(self._store.info_front())
        self._store.enqueue(USER_CARD)
        self._store.enqueue("hello world")
        with self.subTest("Existent record"):
            info = self._store.info_front()
            self.assertIsInstance(info, RecordInfo)
            self.assertEqual(Datatype.DICT, info.datatype)
            self.assertGreaterEqual(datetime.fromisoformat(self._store.now()),
                                    datetime.fromisoformat(info.created_at))

    def test_info_back_method(self):
        with self.subTest("Non existent record"):
            self.assertIsNone(self._store.info_back())
        self._store.enqueue("hello world")
        self._store.enqueue(USER_CARD)
        with self.subTest("Existent record"):
            info = self._store.info_back()
            self.assertIsInstance(info, RecordInfo)
            self.assertEqual(Datatype.DICT, info.datatype)
            self.assertGreaterEqual(datetime.fromisoformat(self._store.now()),
                                    datetime.fromisoformat(info.created_at))

    def test_count_records_method(self):
        with self.subTest("Test that new store is empty"):
            self.assertEqual(0, self._store.count_records())
        with self.subTest("Test that store contains 1 item"):
            self._store.enqueue(USER_CARD)
            self.assertEqual(1, self._store.count_records())

    def test_count_bytes_method(self):
        size_of_user = len(paradict.pack(USER_CARD))
        # set data
        self._store.enqueue(USER_CARD)
        self._store.enqueue(USER_CARD)
        # count bytes in the store
        with self.subTest():
            r = self._store.count_bytes()
            expected = size_of_user * 2
            self.assertEqual(expected, r)

    def test_count_front_bytes_method(self):
        size_of_user = len(paradict.pack(USER_CARD))
        # set data
        self._store.enqueue(USER_CARD)
        self._store.enqueue(EMPTY_USER_CARD)
        # count bytes of the item at front
        with self.subTest():
            r = self._store.count_front_bytes()
            expected = size_of_user
            self.assertEqual(expected, r)

    def test_count_back_bytes_method(self):
        size_of_user = len(paradict.pack(USER_CARD))
        # set data
        self._store.enqueue(EMPTY_USER_CARD)
        self._store.enqueue(USER_CARD)
        # count bytes of the item at front
        with self.subTest():
            r = self._store.count_back_bytes()
            expected = size_of_user
            self.assertEqual(expected, r)

    def test_is_empty(self):
        # ---
        with self.subTest("Test that new store is empty"):
            self.assertTrue(self._store.is_empty())
        # ---
        with self.subTest("Test that new store is not empty"):
            self._store.enqueue(USER_CARD)
            self.assertFalse(self._store.is_empty())

    def test_enqueue_method(self):
        with self.subTest("Test empty queue store"):
            self.assertEqual(0, self._store.count_records())
        with self.subTest("Test queue store after populating it"):
            self._store.enqueue(USER_CARD)
            self.assertEqual(1, self._store.count_records())
            self._store.enqueue(EMPTY_USER_CARD)
            self.assertEqual(2, self._store.count_records())

    def test_enqueue_many_method(self):
        r = self._store.enqueue_many((10, 11, 12, 13))
        expected = (1, 2, 3, 4)
        self.assertEqual(expected, r)
        self.assertEqual(4, self._store.count_records())

    def test_dequeue_method(self):
        with self.subTest("Test empty queue store"):
            self.assertIsNone(self._store.dequeue())
        with self.subTest("Test empty queue store with default value on"):
            self.assertEqual(USER_CARD, self._store.dequeue(default=USER_CARD))
        with self.subTest("Test enqueue then dequeue"):
            self._store.enqueue(EMPTY_USER_CARD)
            self._store.enqueue(USER_CARD)
            self.assertEqual(2, self._store.count_records())
            self.assertEqual(EMPTY_USER_CARD, self._store.dequeue())
            self.assertEqual(1, self._store.count_records())
            self.assertEqual(USER_CARD, self._store.dequeue())
            self.assertEqual(0, self._store.count_records())

    def test_peek_front_method(self):
        with self.subTest("Test empty queue store"):
            self.assertIsNone(self._store.peek_front())
        with self.subTest("Test empty queue store with default value on"):
            self.assertEqual(USER_CARD, self._store.peek_front(default=USER_CARD))
        with self.subTest("Test queue store after populating it"):
            self._store.enqueue(EMPTY_USER_CARD)
            self._store.enqueue(USER_CARD)
            self.assertEqual(EMPTY_USER_CARD, self._store.peek_front())
            self._store.dequeue()
            self.assertEqual(USER_CARD, self._store.peek_front())
            self.assertEqual(1, self._store.count_records())

    def test_peek_back_method(self):
        with self.subTest("Test empty queue store"):
            self.assertIsNone(self._store.peek_back())
        with self.subTest("Test empty queue store with default value on"):
            self.assertEqual(USER_CARD, self._store.peek_back(default=USER_CARD))
        with self.subTest("Test queue store after populating it"):
            self._store.enqueue(EMPTY_USER_CARD)
            self.assertEqual(EMPTY_USER_CARD, self._store.peek_back())
            self._store.enqueue(USER_CARD)
            self.assertEqual(USER_CARD, self._store.peek_back())
            self.assertEqual(2, self._store.count_records())

    def test_get_front_rowid(self):
        rowid1 = self._store.enqueue(USER_CARD)
        rowid2 = self._store.enqueue(USER_CARD)
        self.assertEqual(rowid1, self._store.front_uid())

    def test_get_back_rowid(self):
        rowid1 = self._store.enqueue(USER_CARD)
        rowid2 = self._store.enqueue(USER_CARD)
        self.assertEqual(rowid2, self._store.back_uid())


class TestSmallestChunkSize(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        smallest_chunk_size = 1
        self._jinbase = Jinbase(self._filename,
                                chunk_size=smallest_chunk_size)
        self._store = self._jinbase.queue

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        with self.subTest("Test empty queue store"):
            self.assertEqual(0, self._store.count_records())
        with self.subTest("Test queue store after populating it"):
            self._store.enqueue(USER_CARD)
            self.assertEqual(1, self._store.count_records())
            self._store.enqueue(EMPTY_USER_CARD)
            self.assertEqual(2, self._store.count_records())
        with self.subTest("Test dequeue"):
            r = self._store.dequeue()
            self.assertEqual(USER_CARD, r)
            self.assertEqual(1, self._store.count_records())
            r = self._store.dequeue()
            self.assertEqual(EMPTY_USER_CARD, r)
            self.assertEqual(0, self._store.count_records())

    def test_count_front_chunks_method(self):
        self._store.enqueue(USER_CARD)
        self._store.enqueue(EMPTY_USER_CARD)
        size_user_card = len(paradict.pack(USER_CARD))  # n bytes
        size_empty_user_card = len(paradict.pack(EMPTY_USER_CARD))  # n bytes
        # count total chunks
        with self.subTest("Count total chunks"):
            n_chunks = self._store.count_chunks()
            expected_n_chunks = size_user_card + size_empty_user_card
            self.assertEqual(expected_n_chunks, n_chunks)
        # count front chunks
        with self.subTest("Count chunks at front"):
            n_chunks = self._store.count_front_chunks()
            expected_n_chunks = size_user_card
            self.assertEqual(expected_n_chunks, n_chunks)
        # dequeue then count total chunks
        with self.subTest("Dequeue then count total chunks"):
            self._store.dequeue()
            n_chunks = self._store.count_chunks()
            expected_n_chunks = size_empty_user_card
            self.assertEqual(expected_n_chunks, n_chunks)

    def test_count_back_chunks_method(self):
        self._store.enqueue(EMPTY_USER_CARD)
        self._store.enqueue(USER_CARD)
        size_user_card = len(paradict.pack(USER_CARD))  # n bytes
        size_empty_user_card = len(paradict.pack(EMPTY_USER_CARD))  # n bytes
        # count total chunks
        with self.subTest("Count total chunks"):
            n_chunks = self._store.count_chunks()
            expected_n_chunks = size_user_card + size_empty_user_card
            self.assertEqual(expected_n_chunks, n_chunks)
        # count back chunks
        with self.subTest("Count chunks at back"):
            n_chunks = self._store.count_back_chunks()
            expected_n_chunks = size_user_card
            self.assertEqual(expected_n_chunks, n_chunks)
        # dequeue then count total chunks
        with self.subTest("Dequeue then count total chunks"):
            self._store.dequeue()
            n_chunks = self._store.count_chunks()
            expected_n_chunks = size_user_card
            self.assertEqual(expected_n_chunks, n_chunks)


class TestDefaultValue(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        smallest_chunk_size = 1  # 1 byte
        self._jinbase = Jinbase(self._filename,
                                chunk_size=smallest_chunk_size)
        self._store = self._jinbase.queue

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        self.assertEqual(USER_CARD, self._store.dequeue(default=USER_CARD))
        self.assertEqual(USER_CARD, self._store.peek_front(default=USER_CARD))
        self.assertEqual(USER_CARD, self._store.peek_back(default=USER_CARD))


class TestTransactionContext(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)
        self._store = self._jinbase.queue

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        with self._store.transaction():  # TransactionMode.IMMEDIATE by default
            self._store.enqueue(USER_CARD)
            self._store.enqueue(USER_CARD)
            self._store.dequeue()


class TestLargeBinaryData(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)
        self._store = self._jinbase.queue

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        data = b'\x00' * (const.CHUNK_SIZE * 2)
        self._store.enqueue(data)
        self.assertEqual(data, self._store.dequeue())


if __name__ == "__main__":
    unittest.main()
