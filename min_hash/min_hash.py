import os
import subprocess
import simhash
import argparse

from datasketch import MinHash
from urllib.parse import urlparse
from warcio.archiveiterator import ArchiveIterator



class Minhash:
    def __init__(self, input):
        self.__archive = ArchiveHandler

        print(self.__archive(input).archive)

    @staticmethod
    def update_minhash_set(data, minhash_set=None):
        """ This updates a minhash set. If no set is given, a new one will be created and returned. Otherwise the given
            minhash set is updated.

        :param data:
        :param minhash_set:
        :return:
        """
        if not minhash_set:
            minhash_set = MinHash()

        if not type(data) == type(list()):
            raise TypeError("Received {} but expected list instead!".format(type(data)))

        return minhash_set.update(data.encode('utf8'))

    @staticmethod
    def calc_jaccard_similarity(set1, set2):
        """ This calculates the jaccard similarity between set1 and set2.

        :param set1:
        :param set2:
        :return:
        """
        s1, s2 = set(set1), set(set2)
        return float(len(s1.intersection(s2)))/float(len(s1.union(s2)))


class ArchiveHandler:
    def __init__(self, path):
        self.__path = path
        self.__archive = self.__get_archive(path)

    @property
    def archive(self):
        """

        :return:
        """
        return self.__archive

    def __get_archive(self, path, size=None):
        """

        :param path:
        :return:
        """
        size = None  # Not implemented
        res = list()

        #if self.__is_url(path):
        #    try:
        #        subprocess.check_call(path)
        #    except subprocess.CalledProcessError as err:
        #        print(err)
        #        return None

        if os.path.isfile(path):
            with open(path, 'rb') as stream:
                for record in ArchiveIterator(stream):
                    if record.rec_type == 'response':
                        res.append(record)

        return res

    @staticmethod
    def __is_url(url):
        """ Checks if link is an URL.

        :param url:
        :return:
        """

        try:
            urlparse(url)
            return True
        except:
            return False

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="file or link to an archive")

if __name__ == "__main__":
    m = Minhash(parser.parse_args().input)

