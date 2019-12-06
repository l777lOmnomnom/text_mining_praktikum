import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from lib import data_handler


class Minhash:
    def __init__(self, config):
        self.data_handler = data_handler.DataHandlerMinHash()

        self.__input = config.get("archive")
        self.__database = config.get("database")
        self.__elements = config.get("elements", 1000)
        self.__offset = config.get("offset", 0)
        self.__all = config.get("all", False)

    @property
    def elements(self):
        return self.__elements

    @property
    def offset(self):
        return self.__offset

    @offset.setter
    def offset(self, _o):
        self.__offset = _o

    @property
    def input(self):
        return self.__input

    @input.setter
    def input(self, __i):
        self.__input = __i

    @property
    def database(self):
        return self.__database

    @database.setter
    def database(self, __d):
        self.__database = __d

    def update_hash_db(self):
        """ This updates the hash data base with new min hash sets

        :return:
        """
        hash_db = self.data_handler.get_hash_list(self.input, self.elements)
        self.data_handler.update_database(hash_db, "min_hash")

        return

    def estimate_jaccard_sim(self, data):
        """ This estimates the jaccard similarity between all entries in a set of min hashes. The results are stored
            in a special database.

        :return:
        """
        est_dict = dict()
        i = 0
        for offset1, hash1 in data.items():
            i += 1
            j = 0
            for offset2, hash2 in data.items():
                j += 1
                if j > i:
                    est_dict.update({"{}#{}".format(offset1, offset2): self.__estimate_jaccard_sim(hash1, hash2)})

        return

    @staticmethod
    def __estimate_jaccard_sim(minhash1, minhash2):
        """

        :param body_tuple:
        :return:
        """
        return minhash1.jaccard(minhash2)
