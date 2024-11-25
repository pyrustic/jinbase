"""The Blob class is defined here."""
import os
from jinbase import queries


__all__ = ["Blob"]


class Blob:
    """The Blob class allows a Read access to the blobs of Jinbase records.
    This class isn't intended to be directly instantiated by the user."""
    def __init__(self, store, record_id, n_bytes,
                 n_chunks):
        """
        Initialization.

        [params]
        - store: Store instance.
        - record_id: The record's uid.
        - n_bytes: The size of the blob in bytes.
        - n_chunks: The number of chunks.
        """
        self._store = store
        self._record_id = record_id
        self._n_bytes = n_bytes
        self._n_chunks = n_chunks
        self._dbc = store.dbc
        self._model_name = store.model.name.lower()
        self._chunk_size = store.chunk_size
        self._position = 0
        self._slice_obj = slice(0, 0, 1)
        self._blob_io_files = dict()

    def read(self, length=-1, /):
        """
        Read the blob.

        [params]
        - length: The number of bytes to read.
        Defaults to -1 to mean the entire blob.
        Note that the cursor moves as reads are done.

        [return]
        Returns bytes or an empty byte.
        """
        data = self._read(self._position, length)
        self._position = update_position(self._position, len(data),
                                         os.SEEK_CUR, self._n_bytes)
        return data

    def write(self, data, /):
        """Jinbase doesn't allow Writes on blobs"""
        raise NotImplementedError  # deliberately !

    def tell(self):
        """Returns the current position of the cursor"""
        return self._position

    def seek(self, offset, origin=os.SEEK_SET, /):
        """
        Move the cursor to another position

        [params]
        - offset: Offset value
        - origin: os.SEEK_SET, os.SEEK_CUR, or os.SEEK_END.
        Note that os.SEEK_END referes to position beyond the last
        character of the file, not the last character itself.
        """
        self._position = update_position(self._position,
                                         offset, origin,
                                         self._n_bytes)

    def close(self):
        """Close this Blob instance. Note that this method
        is automatically called by the Store's open_blob method.
        """
        for blob_io_file in self._blob_io_files.values():
            try:
                blob_io_file.close()
            except Exception as e:
                pass

    def _read(self, position, length):
        if length == 0 or position == self._n_chunks:
            return b''
        elif length < -1:
            msg = "Invalid length."
            raise ValueError(msg)
        start = position
        stop = self._n_bytes - 1 if length == -1 else start + length - 1
        stop = self._n_bytes -1 if stop >= self._n_bytes else stop
        blob_slices = get_blob_slices(start, stop, self._chunk_size)
        blob_slices = [blob_slice for blob_slice in blob_slices if blob_slice[0] <= self._n_chunks]
        if len(blob_slices) == 1:
            blob_slice = blob_slices[0]
            data = self._get_chunk(blob_slice)
        else:
            buffer = bytearray()
            for blob_slice in blob_slices:
                chunk = self._get_chunk(blob_slice)
                buffer.extend(chunk)
            data = bytes(buffer)
        return data

    def _get_blob_io_file(self, chunk_index):
        try:
            blob_io_file = self._blob_io_files[chunk_index]
        except KeyError as e:
            with self._dbc.cursor() as cur:
                sql = queries.GET_CHUNK_ID.format(model=self._model_name,
                                                  offset=chunk_index)
                cur.execute(sql, (self._record_id,))
                r = cur.fetchone()
                if r is None:
                    msg = "Failed to get 'chunk_id' for record {}".format(self._record_id)
                    raise Exception(msg)
                chunk_id = r[0]
                table_name = "jinbase_{}_data".format(self._model_name)
                blob_io_file = self._dbc.blobopen(table_name, "chunk", chunk_id)
                self._blob_io_files[chunk_index] = blob_io_file
        return blob_io_file

    def _get_chunk(self, blob_slice):
        chunk_index, slice_obj = blob_slice
        if chunk_index == self._n_chunks:
            return b''
        elif chunk_index > self._n_chunks:
            msg = "BLOB index out of range for record {} (UID).".format(self._record_id)
            raise IndexError(msg)
        blob_io_file = self._get_blob_io_file(chunk_index)
        chunk = blob_io_file[slice_obj]
        return chunk

    def __getitem__(self, index):
        if isinstance(index, slice):
            slice_obj = index
        else:
            index = self._n_bytes + index if index < 0 else index
            slice_obj = slice(index, index + 1)
        slice_start, slice_stop, slice_step = slice_obj.indices(self._n_bytes)
        if slice_step != 1:
            msg = "The slice object should have 1 as step value."
            raise ValueError(msg)
        return self._read(slice_start, slice_stop-slice_start)

    def __setitem__(self, index, value):
        raise NotImplementedError  # deliberately !

    def __delitem__(self, index):
        raise NotImplementedError  # deliberately !


def get_blob_slices(start_index, stop_index, chunk_size):
    blob_slices = list()
    chunk_index_1, sub_index_1 = divmod(start_index, chunk_size)
    chunk_index_2, sub_index_2 = divmod(stop_index, chunk_size)
    if start_index == stop_index:
        return ((chunk_index_1, slice(sub_index_2, sub_index_2 + 1)), )
    if chunk_index_1 == chunk_index_2:
        return ((chunk_index_1, slice(start_index, stop_index+1)), )
    blob_slices.append((chunk_index_1, slice(sub_index_1, chunk_size)))
    chunk_index = chunk_index_1
    for i in range(chunk_index_2-chunk_index_1-1):
        chunk_index += 1
        blob_slices.append((chunk_index, slice(0, chunk_size)))
    blob_slices.append((chunk_index+1, slice(0, sub_index_2+1)))
    return tuple(blob_slices)


def update_position(cur_position, offset, origin, n_bytes):
    if origin == os.SEEK_SET:
        if offset < 0:
            msg = "Only positive offset is allowed with os.SEEK_SET."
            raise ValueError(msg)
        new_position = offset
    elif origin == os.SEEK_CUR:
        new_position = cur_position + offset
    elif origin == os.SEEK_END:
        if offset > 0:
            msg = "Only negative offset values are allowed with os.SEEK_END."
            raise ValueError(msg)
        new_position = n_bytes + offset
    else:
        msg = "Unsupported origin value."
        raise ValueError(msg)
    if new_position > n_bytes or new_position < 0:
        msg = "Offset out of range."
        raise ValueError(msg)
    return new_position
