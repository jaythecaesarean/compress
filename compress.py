# python3+
import os
import sys
from pathlib import PurePath
# import zlib, base64
import hashlib
# import zipfile
import shutil


class CompressFile():
    """
    This compresses and archives the file
    The user can choose between zip[default], tar, gztar, bztar, & xztar
    """
    def compress_file(self, filename, output_format="zip"):
        """
        Output: .gz file
        """
        base_name = os.path.splitext(os.path.basename(filename))[0]
        new_archive = shutil.make_archive(
                        base_name=os.getcwd()+'/output/compressed/'+base_name,
                        root_dir=os.getcwd()+"/input/copy/",
                        format=output_format)
        print("Your new compressed file is at: \"{}\"".format(new_archive))
        return new_archive

    def decompress_file(self, filename):
        shutil.unpack_archive(filename=filename,
                              extract_dir="./output/decompressed/")

    def get_file(self):
        filename = str(input("Enter the filename that you want to compress"
                             " or its destination: "))
        file_path = PurePath(filename)
        if os.path.isfile(file_path):
            new_file_path = shutil.copy(file_path, os.getcwd() +
                                        "/input/copy/" +
                                        os.path.basename(filename))
            return new_file_path

        else:
            print("\'{0}\' file does not exists. Make sure that this "
                  "file exists.".format(filename))
            sys.exit(1)

    def choose_ouput_format(self):
        output_format = str(input("Choose a format of the output file (1-6)\n"
                                  "[1]zip (default), [2]tar, [3]gztar,"
                                  "[4]bztar, [5]xztar: "))
        output_dict = {"1": "zip",
                       "2": "tar",
                       "3": "gztar",
                       "4": "bztar",
                       "5": "xztar"}

        chosen_format = output_dict.get(output_format, "")
        if chosen_format:
            return chosen_format
        else:
            print("You entered an invalid number")
            sys.exit(1)

    def get_file_hash(self, filename):
        return hashlib.md5(open(filename, 'rb').read()).hexdigest()


if __name__ == '__main__':
    process = CompressFile()
    filename = process.get_file()
    process.get_file_hash(filename)
    output_format = process.choose_ouput_format()
    compressed_file = process.compress_file(filename, output_format)
    # process.decompress_file(compressed_file)
