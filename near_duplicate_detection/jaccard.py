import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))

from datasketch import MinHash
from lib import data_handler


class JaccardSim:
    def __init__(self, config):
        self.data_handler = data_handler.DataHandlerMinHash(config)

        self.__elements = config.get("elements", 100)
        self.__offset = config.get("offset", 0)
        self.__mode = config.get("mode")
        self.__tracker = 0

        # Currently limited of a small subset of data
        self.__data = dict()

    @property
    def mode(self):
        return self.__mode

    @property
    def tracker(self):
        self.__tracker += 1
        return self.__tracker

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
    def data(self):
        return self.__data

    @data.setter
    def data(self, _d):
        self.__data = _d

    def main(self):
        """

        :return:
        """
        print("Current element size: {}, current offset: {}".format(self.elements, self.offset))
        self.data, is_finished_flag = self.data_handler.get_data(self.elements, self.offset)
        if self.mode == "both_jaccard_sim":
            self.calculate_jaccard_sim()
            self.estimate_jaccard_sim()
        else:
            getattr(self, self.mode)()

        self.offset += self.elements

        while not is_finished_flag:
            print("Current element size: {}, current offset: {}".format(self.elements, self.offset))

            if self.mode == "both_jaccard_sim":
                self.estimate_jaccard_sim()
                self.calculate_jaccard_sim()
            else:
                getattr(self, self.mode)()

            self.offset += self.elements
            self.data, is_finished_flag = self.data_handler.get_data(self.elements, self.offset)

        return

    def estimate_jaccard_sim(self):
        """

        :return:
        """
        sets_dict = dict()
        for source, words in self.data.items():
            m = MinHash()
            for word in words:
                m.update(word.encode('utf8'))
            sets_dict.update({str(source): m})

        datasets = self.__init_dataset(sets_dict)

        for dataset in datasets:
            jaccard_sim = self.__estimate_jaccard_sim(dataset.body_tuple)

            print("Calculations done: {}".format(self.tracker))

            dataset.est_jaccard_sim = jaccard_sim

        self.data_handler.update_database(datasets)

        return

    @staticmethod
    def __estimate_jaccard_sim(body_tuple):
        """

        :param body_tuple:
        :return:
        """
        return body_tuple[0].jaccard(body_tuple[1])

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

        return dataset_list

    def calculate_jaccard_sim(self):
        """

        :return:
        """

        sets_dict = dict()

        for source, words in self.data.items():
            sets_dict.update({str(source): set(words.split(" "))})

        datasets = self.__init_dataset(sets_dict)

        for dataset in datasets:
            jaccard_sim = self.__calculate_jaccard_sim(dataset.body_tuple)

            print("Calculations done: {}".format(self.tracker))

            dataset.calc_jaccard_sim = jaccard_sim

        self.data_handler.update_database(datasets)

        return

    @staticmethod
    def __calculate_jaccard_sim(body_tuple):
        """

        :return:
        """
        return float(len(body_tuple[0].intersection(body_tuple[1]))) / float(len(body_tuple[0].union(body_tuple[1])))

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
