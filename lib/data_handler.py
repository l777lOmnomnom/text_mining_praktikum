from warcio import ArchiveIterator
from bs4 import BeautifulSoup


class DataHandler:
    def __init__(self, source, max_elements=0):
        self.max_elements = max_elements
        self.current_elements = 0

        self.archive = open(source, "r")
        self.archive_stream = ArchiveIterator(self.archive_stream)

    def __iter__(self):
        return self

    def __next__(self):
        text = ""
        valid_record = False

        while not valid_record:
            record = next(self.archive_stream)

            if record.rec_type == 'response' and record.http_headers.get_header('Content-Type') in self.utf_8:
                soup = BeautifulSoup(record.content_stream(), 'lxml', from_encoding='utf-8')
                for script in soup(["script", "style"]):
                    script.extract()

                try:
                    text = soup.body.get_text(separator=' ')
                    text = "\n".join([line.strip() for line in text.split("\n") if line.strip() != ""])
                except AttributeError:
                    print('Wrong Encoding at offset ' + str(self.archive_stream.get_record_offset()))
                else:
                    valid_record = True
                    self.current_elements += 1

        yield self.archive_stream.get_record_offset()
        yield text

    def __del__(self):
        try:
            self.archive.close()
            self.archive_stream.close()
        except Exception:
            pass

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
