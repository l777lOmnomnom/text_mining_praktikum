from warcio import ArchiveIterator
from bs4 import BeautifulSoup
import json


class Data:
    def __init__(self, source):
        self.current_elements = 0
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
        Returns the next entry in the warc.io archive.

        :return: int(), str() - offset, text
        """
        text = ""
        valid_record = False

        #while not valid_record:
        #    print("no valid record")
        """
            try:
                print(self.__archive_stream)
                print(next(self.__archive_stream))
                record = next(self.__archive_stream)
                print(record)
            except Exception as err:
                print(err)
                text = "Asd"
            else:
                if record.rec_type == 'response' and record.http_headers.get_header('Content-Type') in self.utf_8:
                    soup = BeautifulSoup(record.content_stream(), 'lxml', from_encoding='utf-8')
                    for script in soup(["script", "style"]):
                        script.extract()

                    try:
                        text = soup.body.get_text(separator=' ')
                        text = "\n".join([line.strip() for line in text.split("\n") if line.strip() != ""])
                    except AttributeError:
                        print('Wrong Encoding at offset ' + str(self.__archive_stream.get_record_offset()))
                    else:
                        valid_record = True
                        self.current_elements += 1
            if i == 5:
                break
            i += 1
        return self.__archive_stream.get_record_offset(), text
        """

        """
        print(self.source)
        __archive = open(self.source, "r")
        __archive_stream = ArchiveIterator(__archive)

        for record in __archive_stream:
            if record.rec_type == 'response' and record.http_headers.get_header('Content-Type') in self.utf_8:
                soup = BeautifulSoup(record.content_stream(), 'lxml', from_encoding='utf-8')
                for script in soup(["script", "style"]):
                    script.extract()

                try:
                    text = soup.body.get_text(separator=' ')
                    text = "\n".join([line.strip() for line in text.split("\n") if line.strip() != ""])
                except AttributeError:
                    print('Wrong Encoding at offset ' + str(__archive_stream.get_record_offset()))
                else:
                    valid_record = True
                    self.current_elements += 1
                    yield __archive_stream.get_record_offset(), text
        """
        with open(self.source, 'r') as tmp:
            records = json.load(tmp)
            for offset, text in records.items():
                self.current_elements += 1
                yield offset, text

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
