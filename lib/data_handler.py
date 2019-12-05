import re
import os
import json
import subprocess
import time
#import pandas as pd
from warcio import ArchiveIterator
import simhash
import re
import ctypes
import json
import time
from bs4 import BeautifulSoup
from datasketch import MinHash
import jsonpickle


# import warcio
# import argparse


class DataHandlerException(Exception):
    """
    This a common convention to have a file specific exception. Usage:

    try:
        your_code()
    except SomeExceptionRaisedByYourCode as err:
        raise DataHandlerException(err)

    It raises the original error but as DataHandlerException to make the failing part more visible
    """
    pass


class __DataHandler:
    @property
    def utf_8(self):
        return ['text/html; charset=UTF-8',
                'text/html; charset=utf-8',
                'text/html;charset=UTF-8',
                'text/html;charset=utf-8',
                'text/html; Charset=UTF-8',
                'text/html; Charset=utf-8;charset=UTF-8',
                'text/html; charset=utf8']

    @staticmethod
    def update_database(new_data, mode, database=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "hash_db")):  # noqa
        """

        :param new_data:
        :param database:
        :return:
        """
        try:
            with open(database, "r") as db:
                data = json.load(db)

        except Exception:
            data = dict()

        for offset, _hash in new_data.items():
            old_entry = data.get(offset, dict())
            new_hash = {"{}_hash".format(mode): jsonpickle.encode(_hash)}
            new_entry = old_entry.update(new_hash)

            data.update({offset: new_entry})

        with open(database, "w") as db:
            json.dump(data, db)

    def get_hash_list(self, input_file, elements=1000, offset=0):
        """

        :return:
        """
        i = 0
        hash_list = []
        hash_db = dict()

        start_time = time.time()
        with open("/home/omnomnom/git/text_mining/data/archives/de_web_2019.01000.warc.gz", 'rb') as stream:
            archive_stream = ArchiveIterator(stream)
            for record in archive_stream:
                if record.rec_type == 'response' and record.http_headers.get_header('Content-Type') in self.utf_8:
                    soup = BeautifulSoup(record.content_stream(), 'lxml', from_encoding='utf-8')
                    for script in soup(["script", "style"]):
                        script.extract()

                    try:
                        text = soup.body.get_text(separator=' ')
                        lines = (line.strip() for line in text.splitlines())
                        # break multi-headlines into a line each
                        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                        # drop blank lines
                        text = '\n'.join(chunk for chunk in chunks if chunk)

                    except AttributeError as err:
                        print('Wrong Encoding at offset ' + str(archive_stream.get_record_offset()))
                    else:
                        i += 1
                        _hash = self.hash(text)

                        offset = archive_stream.get_record_offset()

                        hash_list.append(_hash)
                        hash_db.update({offset: _hash})

                        print("{} / {} hashes created".format(i, elements))

                        self.update_database(hash_db, self.mode)

                # TODO: Implement an offset counter
                # Stop if max elements is reached
                if i > elements:
                    archive_stream.close()
                    break

        return hash_list

    def hash(self, text):
        raise ModuleNotFoundError("Dont call the base class ...")


class DataHandlerSimHash(__DataHandler):
    def __init__(self):
        super(DataHandlerSimHash, self).__init__()
        self.mode = "simhash"

    def get_hash_list(self, input_file, elements=1000, offset=0):
        super().get_hash_list(input_file, elements, offset)

    def hash(self, text):
        shingles = (' '.join(tokens) for tokens in simhash.shingle(self.tokenize(text), 3))

        return simhash.compute([ctypes.c_ulong(hash(shingle)).value for shingle in shingles])

    @staticmethod
    def tokenize(text):
        tokens = re.split("\s+", re.sub(r'[^\w\s]', '', text.lower()))
        # print(tokens)
        return tokens


class DataHandlerMinHash(__DataHandler):
    def __init__(self):
        super(DataHandlerMinHash, self).__init__()
        self.mode = "minhash"

    def get_hash_list(self, input_file, elements=1000, offset=0):
        super().get_hash_list(input_file, elements, offset)

    def hash(self, text):
        """

        :param text:
        :return:
        """
        m = None
        for words in text.split("\n"):
            m = MinHash()

            for word in words:
                m.update(word.encode('utf8'))

        return m

    @staticmethod
    def __read_source(input_file, elements, offset=0):
        """
        Reads data from an extracted or compressed warc archive (.source | .warc.gz) and returns a dictonary with
        {source_address1: source_body1, ...}
        If elements if given it will only read so many entries until the given amount is reached.
        If offset if given the returned entries will start with an offset of entries shifted.
        This can be used to iterate through the data without using to much storage.

        :param input_file: path of the extracted source file
        :param elements: the amount of elements you want to retrieve
        :param offset: the offset from the beginning of the file
        :return: result_dict
        """
        line = None  # Placeholder
        is_finished_flag = False
        return_dict = dict()

        with open(input_file, 'r') as source:
            current_elements = 0
            skipped_elements = 0
            source_iterator = iter(source)
            try:
                # Offsets the iterator
                if offset != 0:
                    while skipped_elements <= int(offset):
                        line = next(source_iterator)
                        if re.search("<source><location>", line):
                            skipped_elements += 1

                    # Otherwise the header wouldn't be available bellow as the next method continues
                    header = line.split("</location>")[0].replace("<source><location>", "")

                # Create the actual dict with the data extries from offset to elements + offset
                while current_elements < elements:
                    line = next(source_iterator)

                    if re.search("<source><location>", line):
                        header = line.split("</location>")[0].replace("<source><location>", "")
                        current_elements += 1

                        os.system("clear")
                        print("Got element {}".format(current_elements + offset))
                    #  This is stupid but it works
                    elif line is "\n" or id(line) == 140591544343968:
                        continue

                    else:
                        body = return_dict.get(header, "")
                        return_dict.update({header: "{} {}".format(body, line)})
            except StopIteration:
                is_finished_flag = True
                return return_dict, is_finished_flag
            except Exception as err:
                raise DataHandlerException(err)

        return return_dict, is_finished_flag

    # Somehow there is a problem with pathfinding here
    @staticmethod
    def __extract_archive(input_file, output_file="/tmp/output.source"):
        """
        Extracts a warc.gz file. Can also be called from command line via :

        $ python3 datahandler.py -i input_file -o output_file

        :param input_file: Path to the warc.gz archive
        :param output_file: Path to the destination file (default: /tmp/output.source)
        :return:
        """
        current_file_loc = os.path.dirname(os.path.abspath(__file__))

        if not os.path.isfile(input_file):
            raise FileNotFoundError("File {} not found!".format(input_file))

        if os.path.isfile(output_file):
            print("Found existing output file ({}). Renaming it to {}.old and continue ...".format(output_file,
                                                                                                   output_file))
            os.rename(output_file, "{}.old".format(output_file))

        tool_path = os.path.join(current_file_loc, '..', 'tools', 'jwarcex-standalone-2.0.0.jar')
        cmd = "java -jar {} {} {} -c".format(tool_path, input_file, output_file)

        print(cmd)

        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as err:
            print("It looks like there is an issue with path-finding. Copy the link and execute it manually ...")
            print("There was an errror executing the command. Stopping now!")
            print(err)
            exit(1)
        else:
            print("Successfully extracted {} to {}!".format(input_file, output_file))

        return output_file
