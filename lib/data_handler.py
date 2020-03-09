from warcio import ArchiveIterator
from bs4 import BeautifulSoup


class Data:
    def __init__(self):
        self.current_elements = 0
        self.__archive = None
        self.__archive_stream = None

    def __iter__(self):
        return self

    def __del__(self):
        try:
            self.__archive.close()
            self.__archive_stream.close()
        except Exception as err:
            print("Got {} while closing Archive!".format(err))

    def __next__(self):
        text = ""
        valid_record = False

        while not valid_record:
            record = next(self.__archive_stream)

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

        yield self.__archive_stream.get_record_offset()
        yield text

    def read_in(self, source):
        """

        :return:
        """
        self.__archive = open(source, "r")
        self.__archive_stream = ArchiveIterator(self.__archive_stream)

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
