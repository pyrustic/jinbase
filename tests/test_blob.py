import os
import unittest
from jinbase.blob import get_blob_slices, update_position


class TestGetBlobSlicesFunction(unittest.TestCase):
    """
    1           2           3           4           5
    0 1 2 3 4   0 1 2 3 4   0 1 2 3 4   0 1 2 3 4   0 1 2 3 4
    """
    def test(self):
        chunk_size = 5
        with self.subTest():
            start_index, stop_index = 0, 1
            r = get_blob_slices(start_index, stop_index, chunk_size)
            expected = ((0, slice(0, 2)),)
            self.assertEqual(expected, r)
        with self.subTest():
            start_index, stop_index = 0, 4
            r = get_blob_slices(start_index, stop_index, chunk_size)
            expected = ((0, slice(0, 5)),)
            self.assertEqual(expected, r)
        with self.subTest():
            start_index, stop_index = 0, 6
            r = get_blob_slices(start_index, stop_index, chunk_size)
            expected = ((0, slice(0, 5)), 
                        (1, slice(0, 2)))
            self.assertEqual(expected, r)
        with self.subTest():
            start_index, stop_index = 0, 13
            r = get_blob_slices(start_index, stop_index, chunk_size)
            expected = ((0, slice(0, 5)),
                        (1, slice(0, 5)),
                        (2, slice(0, 4)))
            self.assertEqual(expected, r)
        with self.subTest():
            start_index, stop_index = 6, 13
            r = get_blob_slices(start_index, stop_index, chunk_size)
            expected = ((1, slice(1, 5)),
                        (2, slice(0, 4)))
            self.assertEqual(expected, r)
        with self.subTest():
            start_index, stop_index = 6, 18
            r = get_blob_slices(start_index, stop_index, chunk_size)
            expected = ((1, slice(1, 5)),
                        (2, slice(0, 5)),
                        (3, slice(0, 4)))
            self.assertEqual(expected, r)

    def test_start_equals_stop(self):
        chunk_size = 5
        with self.subTest():
            start_index, stop_index = 0, 0
            r = get_blob_slices(start_index, stop_index, chunk_size)
            expected = ((0, slice(0, 1)), )
            self.assertEqual(expected, r)
        with self.subTest():
            start_index, stop_index = 1, 1
            r = get_blob_slices(start_index, stop_index, chunk_size)
            expected = ((0, slice(1, 2)),)
            self.assertEqual(expected, r)
        with self.subTest():
            start_index, stop_index = 5, 5
            r = get_blob_slices(start_index, stop_index, chunk_size)
            expected = ((1, slice(0, 1)), )
            self.assertEqual(expected, r)
        with self.subTest():
            start_index, stop_index = 18, 18
            r = get_blob_slices(start_index, stop_index, chunk_size)
            expected = ((3, slice(3, 4)),)
            self.assertEqual(expected, r)


class TestUpdatePositionFunction(unittest.TestCase):

    def test_with_seek_set_origin(self):
        n_bytes = 20
        with self.subTest("Offset equals 0"):
            cur_position = 5
            offset, origin = 0, os.SEEK_SET
            r = update_position(cur_position, offset, origin, n_bytes)
            expected = 0
            self.assertEqual(expected, r)
        with self.subTest("Offset is positive"):
            cur_position = 5
            offset, origin = 1, os.SEEK_SET
            r = update_position(cur_position, offset, origin, n_bytes)
            expected = 1
            self.assertEqual(expected, r)
        with self.subTest("Offset is negative"):
            cur_position = 5
            offset, origin = -1, os.SEEK_SET
            with self.assertRaises(ValueError):
                update_position(cur_position, offset, origin, n_bytes)
        with self.subTest("Offset to end of file"):
            cur_position = 5
            offset, origin = n_bytes, os.SEEK_SET
            r = update_position(cur_position, offset, origin, n_bytes)
            expected = n_bytes
            self.assertEqual(expected, r)
        with self.subTest("Offset is out of range"):
            cur_position = 5
            offset, origin = n_bytes+1, os.SEEK_SET
            with self.assertRaises(ValueError):
                update_position(cur_position, offset, origin, n_bytes)

    def test_with_seek_cur_origin(self):
        n_bytes = 20
        with self.subTest("Offset equals 0"):
            cur_position = 5
            offset, origin = 0, os.SEEK_CUR
            r = update_position(cur_position, offset, origin, n_bytes)
            expected = 5
            self.assertEqual(expected, r)
        with self.subTest("Offset is positive"):
            cur_position = 5
            offset, origin = 1, os.SEEK_CUR
            r = update_position(cur_position, offset, origin, n_bytes)
            expected = 6
            self.assertEqual(expected, r)
        with self.subTest("Offset is negative"):
            cur_position = 5
            offset, origin = -1, os.SEEK_CUR
            r = update_position(cur_position, offset, origin, n_bytes)
            expected = 4
            self.assertEqual(expected, r)
        with self.subTest("Offset to end of file"):
            cur_position = 5
            offset, origin = n_bytes - cur_position, os.SEEK_CUR
            r = update_position(cur_position, offset, origin, n_bytes)
            expected = n_bytes
            self.assertEqual(expected, r)
        with self.subTest("Offset is out of range"):
            cur_position = 5
            offset, origin = n_bytes - cur_position +1, os.SEEK_CUR
            with self.assertRaises(ValueError):
                update_position(cur_position, offset, origin, n_bytes)

    def test_with_seek_end_origin(self):
        n_bytes = 20
        with self.subTest("Offset equals 0"):
            cur_position = 5
            offset, origin = 0, os.SEEK_END  # end of file
            r = update_position(cur_position, offset, origin, n_bytes)
            expected = n_bytes
            self.assertEqual(expected, r)
        with self.subTest("Offset is positive"):
            cur_position = 5
            offset, origin = 1, os.SEEK_END
            with self.assertRaises(ValueError):
                update_position(cur_position, offset, origin, n_bytes)
        with self.subTest("Offset is negative"):
            cur_position = 5
            offset, origin = -1, os.SEEK_END
            r = update_position(cur_position, offset, origin, n_bytes)
            expected = n_bytes - 1
            self.assertEqual(expected, r)
        with self.subTest("Offset to begin of file"):
            cur_position = 5
            offset, origin = -n_bytes, os.SEEK_END
            r = update_position(cur_position, offset, origin, n_bytes)
            expected = 0
            self.assertEqual(expected, r)
        with self.subTest("Offset is out of range"):
            cur_position = 5
            offset, origin = -n_bytes-1, os.SEEK_END
            with self.assertRaises(ValueError):
                update_position(cur_position, offset, origin, n_bytes)


if __name__ == "__main__":
    unittest.main()
