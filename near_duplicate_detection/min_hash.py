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

    @staticmethod
    def __init_dataset(dataset):
        """

        :param dataset:
        :return:
        """
        dataset_list = list()

        i = 0
        for header1, body1 in dataset.items():
            i += 1
            j = 0
            for header2, body2 in dataset.items():
                j += 1
                if j > i:
                    dataset_list.append(Dataset(header1, header2, body1, body2))
                print("{} cross product data sets created".format(i*j))
        return dataset_list


class Dataset:
    def __init__(self, header1, header2, body1, body2):
        self.__header_tuple = "{}#{}".format(header1, header2)
        self.__body_tuple = (body1, body2)
        self.__est_jaccard_sim = None
        self.__calc_jaccard_sim = None
        self.__est_jaccard_time = None  # Not implemented
        self.__calc_jaccard_time = None  # Not implemented

    @property
    def header_tuple(self):
        return self.__header_tuple

    @property
    def body_tuple(self):
        return self.__body_tuple

    @property
    def est_jaccard_sim(self):
        return self.__est_jaccard_sim

    @property
    def calc_jaccard_sim(self):
        return self.__calc_jaccard_sim

    @property
    def est_jaccard_time(self):
        return self.__est_jaccard_time

    @property
    def calc_jaccard_time(self):
        return self.__calc_jaccard_time

    @est_jaccard_sim.setter
    def est_jaccard_sim(self, sim):
        self.__est_jaccard_sim = sim

    @calc_jaccard_sim.setter
    def calc_jaccard_sim(self, sim):
        self.__calc_jaccard_sim = sim

    def dump(self):
        return {self.header_tuple: {"est_jaccard_sim": self.est_jaccard_sim}}
