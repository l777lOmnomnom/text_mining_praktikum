import time
from warcio import ArchiveIterator
import simhash
import re
import ctypes
from bs4 import BeautifulSoup
from datasketch import MinHash


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


class DataHandler:
    def __init__(self):
        self.mode = None

    @property
    def utf_8(self):
        """
        This is the utf_8 encoding the DataHandler uses.
        :return:
        """
        return ['text/html; charset=UTF-8',
                'text/html; charset=utf-8',
                'text/html;charset=UTF-8',
                'text/html;charset=utf-8',
                'text/html; Charset=UTF-8',
                'text/html; Charset=utf-8;charset=UTF-8',
                'text/html; charset=utf8']

    def get_hash_db(self, input_file, _simhash, _minhash, elements=1000):
        """
        This calculates the hashes for a given archive.

        :param input_file: the input archive
        :param _simhash: Marks if simhashes should be calculated
        :param _minhash: Marks if minhashes should be calculated
        :param elements: the amount of elements retrieved at once

        :return: hash data base as {offset: {"min_hash": {minhash, "sim_hash": simhash}}
        """
        if not _simhash and not _minhash:
            raise DataHandlerException("No mode")

        i = 0
        hash_db = dict()

        minhash_time = 0
        simhash_time = 0

        with open(input_file, 'rb') as stream:
            archive_stream = ArchiveIterator(stream)
            for record in archive_stream:
                # This is some shananigan from alex
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
                        offset = archive_stream.get_record_offset()

                        hashes = dict()
                        if _simhash:
                            start = time.time()
                            _hash = self.simhash(text)
                            simhash_time = simhash_time + time.time() - start
                            hashes.update({"simhash": _hash})

                        if _minhash:
                            start = time.time()
                            _hash = self.minhash(text)
                            hashes.update({"minhash": _hash})
                            minhash_time = minhash_time + time.time() - start

                        hash_db.update({offset: hashes})

                # TODO: Implement an offset counter
                # Stop if max elements is reached
                if i >= elements:
                    archive_stream.close()
                    break

        if _simhash:
            print("Simhashing {} elements took {} seconds".format(elements, simhash_time))
        if _minhash:
            print("Minhashing {} elements took {} seconds".format(elements, minhash_time))

        return hash_db

    def minhash(self, text):
        """
        Creates a min-hash for a given text by updating a MinHash with every word contained in the text.

        :param text: the string which should be hashed
        :return: MinHash()
        """
        m = None

        for words in text.split("\n"):
            m = MinHash()

            for word in words:
                m.update(word.encode('utf8'))

        return m

    def simhash(self, text):
        shingles = (' '.join(tokens) for tokens in simhash.shingle(self.tokenize(text), 6))
        s = simhash.compute([ctypes.c_ulong(hash(shingle)).value for shingle in shingles])
        return s

    @staticmethod
    def tokenize(text):
        tokens = re.split("\s+", re.sub(r'[^\w\s]', '', text.lower()))
        # print(tokens)
        return tokens