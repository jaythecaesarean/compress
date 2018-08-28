import unittest
# from test import support
import string
import random
# from unittest.mock import MagicMock
from compress import CompressFile
# import io
# from unittest import mock
import os
import shutil
from pathlib import PurePath


class CompressionTest(unittest.TestCase):
    # create a new file_test.txt
    # note: every test below creates a file with random context
    orig_hash = ""

    def setUp(self):
        random_string = ""
        for char in range(0, 1000):
            random_string += random.choice(string.printable)

        self.orig_txt_file = "file_test.txt"
        self.base_name = "file_test"
        self.input_copy_path = os.getcwd() + "/input/copy/"
        self.compressed_path = os.getcwd() + "/output/compressed/"
        self.decompressed_path = os.getcwd() + "/output/decompressed/"
        txt_file = open(self.orig_txt_file, "w")
        txt_file.write(random_string)
        txt_file.close()

        self.compress = CompressFile()
        self.__class__.orig_hash = self.compress.\
            get_file_hash(self.orig_txt_file)

        # copy the file to the input/copy folder
        self.new_file_path = shutil.copy(PurePath(self.orig_txt_file),
                                         self.input_copy_path +
                                         os.path.basename(self.orig_txt_file))
        # delete created files
        self.addCleanup(os.remove, self.orig_txt_file)
        self.addCleanup(os.remove, self.input_copy_path + "file_test.txt")

    def tearDown(self):
        # remove all created files
        for f in os.listdir(self.compressed_path):
            os.remove(self.compressed_path + f)
        for f in os.listdir(self.decompressed_path):
            os.remove(self.decompressed_path + f)

    def compress_decompress_check(self, output):
        # use the zip to archive the file
        print("creating {} file".format(output))
        newly_compresed = self.compress.compress_file(self.orig_txt_file,
                                                      output)
        # decompress the file
        print("decompressing {} file".format(output))
        self.compress.decompress_file(newly_compresed)
        # compare the hashes from the original to to the decompressed one
        print("orig hash: {}".format(self.__class__.orig_hash))

        new_hash = self.compress.get_file_hash(self.decompressed_path +
                                               self.orig_txt_file)
        print("orig hash: {}".format(self.__class__.orig_hash))
        print("new hash: {}".format(new_hash))
        self.assertEqual(self.__class__.orig_hash, new_hash)

    def test_zip(self):
        self.compress_decompress_check("zip")

    def test_tar(self):
        self.compress_decompress_check("tar")

    def test_gztar(self):
        self.compress_decompress_check("gztar")

    def test_bztar(self):
        self.compress_decompress_check("bztar")

    def test_xztar(self):
        self.compress_decompress_check("xztar")


if __name__ == '__main__':
    unittest.main()
