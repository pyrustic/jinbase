import os.path
import unittest
import tempfile
from datetime import datetime
from litedbc import LiteDBC
from jinbase import Jinbase, Model
from jinbase.store.kv import Kv
from jinbase.store.depot import Depot
from jinbase.store.queue import Queue
from jinbase.store.stack import Stack


class TestEmptyJinbase(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)

    def tearDown(self):
        self._jinbase.close()
        # the Try/Except is needed here because I can only
        # benefit from the constructor's "ignore_cleanup_errors=True"
        # in Python 3.10
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test_properties(self):
        with self.subTest("Test .filename property"):
            self.assertEqual(self._filename, self._jinbase.filename)
        with self.subTest("Test .is_new property"):
            self.assertTrue(self._jinbase.is_new)
        with self.subTest("Test .dbc property"):
            self.assertIsInstance(self._jinbase.dbc, LiteDBC)
        with self.subTest("Test .in_memory property"):
            self.assertFalse(self._jinbase.in_memory)
        with self.subTest("Test .version property"):
            self.assertEqual(1, self._jinbase.version)
        with self.subTest("Test .created_at property"):
            created_at = self._jinbase.created_at  # ISO 8601 datetime string
            now = self._jinbase.now()  # ISO 8601 datetime string
            self.assertGreaterEqual(datetime.fromisoformat(now),
                                    datetime.fromisoformat(created_at))

    def test_stores(self):
        with self.subTest("Test .kv property"):
            self.assertIsInstance(self._jinbase.kv, Kv)
        with self.subTest("Test .depot property"):
            self.assertIsInstance(self._jinbase.depot, Depot)
        with self.subTest("Test .queue property"):
            self.assertIsInstance(self._jinbase.queue, Queue)
        with self.subTest("Test .stack property"):
            self.assertIsInstance(self._jinbase.stack, Stack)

    def test_stats(self):
        with self.subTest("Test .count_records method"):
            self.assertEqual(0, self._jinbase.count_records())
        with self.subTest("Test .count_chunks method"):
            self.assertEqual(0, self._jinbase.count_chunks())
        with self.subTest("Test .count_bytes method"):
            self.assertEqual(0, self._jinbase.count_bytes())

    def test_scan_method(self):
        n_records = n_bytes = 0
        expected = {Model.KV: (n_records, n_bytes),
                    Model.DEPOT: (n_records, n_bytes),
                    Model.QUEUE: (n_records, n_bytes),
                    Model.STACK: (n_records, n_bytes)}
        r = self._jinbase.scan()
        self.assertEqual(expected, self._jinbase.scan())

    def test_latest_method(self):
        user = {"id": 42, "name": "alex"}
        self._jinbase.kv.set("user", user)
        latest_write = self._jinbase.latest()  # ISO 8601 datetime string
        now = self._jinbase.now_dt()
        self.assertGreaterEqual(now, datetime.fromisoformat(latest_write))


class TestJinbaseControl(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test_backup(self):
        kv_store = self._jinbase.kv
        user_data = {"id": 42, "name": "alex"}
        kv_store.set("user", user_data)
        dst_filename = os.path.join(self._tempdir.name, "backup.db")
        self._jinbase.backup(dst_filename)
        jinbase2 = Jinbase(dst_filename)
        kv_store2 = jinbase2.kv
        self.assertEqual(user_data, kv_store2.get("user"))

    def test_vacuum_into(self):
        kv_store = self._jinbase.kv
        user_data = {"id": 42, "name": "alex"}
        kv_store.set("user", user_data)
        dst_filename = os.path.join(self._tempdir.name, "backup.db")
        self._jinbase.vacuum_into(dst_filename)
        jinbase2 = Jinbase(dst_filename)
        kv_store2 = jinbase2.kv
        self.assertEqual(user_data, kv_store2.get("user"))

    def test_close(self):
        self._jinbase.close()
        self.assertTrue(os.path.isfile(self._filename))
        with self.assertRaises(Exception):
            self._jinbase.scan()

    def test_destroy(self):
        self._jinbase.destroy()
        self.assertFalse(os.path.isfile(self._filename))
        with self.assertRaises(Exception):
            self._jinbase.scan()


class TestMultipleJinbaseConnections(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test_copy_method(self):
        user_data1 = {"id": 42, "name": "alex"}
        user_data2 = {"id": 420}
        # jinbase1 get kv store then store item1
        kv_store = self._jinbase.kv
        kv_store.set("user1", user_data1)
        # jinbase2 accesses kv store then read item1
        jinbase2 = self._jinbase.copy()
        kv_store2 = jinbase2.kv
        self.assertEqual(user_data1, kv_store2.get("user1"))
        # jinbase2 stores item2 in kv store
        kv_store2.set("user2", user_data2)
        # jinbase1 reads item2
        self.assertEqual(user_data2, kv_store.get("user2"))


class TestReadonlyJinbase(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        user_data = {"id": 42, "name": "alex"}
        kv_store = self._jinbase.kv
        with self.subTest("Readonly: False"):
            kv_store.set("user", user_data)
            self.assertEqual(user_data, kv_store.get("user"))
        with self.subTest("Readonly: True"):
            jinbase2 = Jinbase(self._filename, is_readonly=True)
            kv_store2 = jinbase2.kv
            self.assertEqual(user_data, kv_store2.get("user"))
            with self.assertRaises(Exception):
                kv_store2.set("user2", {"id": 420})


class TestJinbaseContextManager(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        with Jinbase(self._filename) as jinbase:
            pass
        self.assertTrue(jinbase.is_closed)


class TestTransactionContext(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._jinbase = Jinbase(self._filename)

    def tearDown(self):
        self._jinbase.close()
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        kv_store = self._jinbase.kv
        depot_store = self._jinbase.depot
        queue_store = self._jinbase.queue
        stack_store = self._jinbase.stack
        with self._jinbase.transaction():  # TransactionMode.IMMEDIATE by default
            kv_store.set("user", 42)
            depot_store.append(42)
            queue_store.enqueue(42)
            stack_store.push(42)


if __name__ == "__main__":
    unittest.main()
