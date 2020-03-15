from warcio import ArchiveIterator
from bs4 import BeautifulSoup
import sys


class Data:
    def __init__(self, source):
        self.source = source
        self.__archive = None
        self.__archive_stream = None

    def __iter__(self):
        """
        Returns an iterator of Data()

        :return: Iterator(Data)
        """
        return self

    def __next__(self):
        """
        Returns the next entry in the warc IO archive.

        :return: int(), str() - offset, text
        """
        __archive = open(self.source, "rb")
        __archive_stream = ArchiveIterator(__archive)
        wrong_encoding_list = list()

        current_element = 0
        for record in __archive_stream:
            if record.rec_type == 'response' and record.http_headers.get_header('Content-Type') in self.utf_8:
                soup = BeautifulSoup(record.content_stream(), 'lxml', from_encoding='utf-8')
                for script in soup(["script", "style"]):
                    script.extract()
                try:
                    text = soup.body.get_text(separator=' ')
                    text = "\n".join([line.strip() for line in text.split("\n") if line.strip() != ""])
                except AttributeError:
                    wrong_encoding_list.append(__archive_stream.get_record_offset())
                else:
                    current_element += 1
                    if current_element % 100 == 0:
                        self.__clear_line()
                        print("{} elements hashed ...".format(current_element))
                    yield __archive_stream.get_record_offset(), text

        print('Wrong Encoding at offsets {}'.format(wrong_encoding_list))

    @property
    def utf_8(self):
        """
        This is the utf_8 encoding the DataHandler uses.

        :return: a list of utf8 encodings
        """
        return ['text/html; charset=UTF-8',
                'text/html; charset=utf-8',
                'text/html;charset=UTF-8',
                'text/html;charset=utf-8',
                'text/html; Charset=UTF-8',
                'text/html; Charset=utf-8;charset=UTF-8',
                'text/html; charset=utf8']

    @staticmethod
    def __clear_line():
        """

        :return:
        """
        sys.stdout.write("\033[F")  # back to previous line
        sys.stdout.write("\033[K")  # clear line
