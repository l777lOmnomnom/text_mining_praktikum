import time
import os
import json

from warcio import ArchiveIterator
from bs4 import BeautifulSoup


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
    def __init__(self, source, max_elements=9999999):
        self.length = 0
        self.max_elements = max_elements

        self.__source = source
        self.__text_dict = self.__check_source()

        print("{} elements loaded ...".format(len(self.text_dict)))

        if not self.text_dict:
            raise DataHandlerException("There was an unknown error.\nsource: {}".format(source))

    @property
    def text_dict(self):
        return self.__text_dict

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, new_source):
        self.__source = new_source

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

    def __check_source(self):
        """
        Checks the provides source
            *   if it is a text_entries.json file it will be json encoded and returned as text_dict.
            *   if the source is a warc.gz archive but there exists a text_entries.json with the same name ask for
                a decision if text entries or archive should be used.
                * if text entries call __check_source again with new source (old_source_text_entries.json)
                * else read the archive in and return a text_dict
        :return:  text_dict
        """
        text_dict = None

        if "text_entries" in self.source:
            if os.path.isfile(self.source):
                try:
                    with open(self.source, "r") as file:
                        text_dict = json.load(file)
                except json.JSONDecodeError as err:
                    print("Failed: {}".format(err))
        else:
            text_dict = self.__read_in(self.source)

        if len(text_dict) > self.max_elements:
            while len(text_dict) > self.max_elements:
                text_dict.popitem()

        for text in text_dict.values():
            self.length += len(text)

        return text_dict

    def __read_in(self, source):
        """
        If the source is a warc.gz archives it will be extracted, stripped from whitelines and put into a dict with its
        offset as key and the text as string of lines as value.

        :param source: source warc.gz archive
        :return: text_dict
        """
        if not os.path.isfile(source):
            raise DataHandlerException("Source {} is not a valid file!".format(source))

        with open(source, 'rb') as stream:

            archive_stream = ArchiveIterator(stream)

            text_dict = dict()

            for record in archive_stream:
                if record.rec_type == 'response' and record.http_headers.get_header('Content-Type') in self.utf_8:
                    soup = BeautifulSoup(record.content_stream(), 'lxml', from_encoding='utf-8')
                    for script in soup(["script", "style"]):
                        script.extract()

                    try:
                        text = soup.body.get_text(separator=' ')
                        text = "\n".join([line.strip() for line in text.split("\n") if line.strip() != ""])
                        text_dict.update({archive_stream.get_record_offset(): text})
                    except AttributeError as err:
                        print('Wrong Encoding at offset ' + str(archive_stream.get_record_offset()))

        archive_stream.close()

        with open("{}_text_entries.json".format(source.split(".")[0]), "w") as out:
            json.dump(text_dict, out)

        return text_dict
