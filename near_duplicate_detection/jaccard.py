import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))

from datasketch import MinHash
from lib import data_handler


class JaccardSim:
    def __init__(self, config):
        self.__input_file = config["input"]
        self.__database = config["database"]

        # Currently limited of a small subset of data
        self.__data = data_handler.get_header_body_dict(self.__input_file)

    @property
    def data(self):
        return self.__data

    @property
    def database(self):
        return self.__database

    @staticmethod
    def init_dataset(dataset):
        """

        :param datset:
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
                    dataset_list.append(Dataset(header1, header2 ,body1, body2))

        return dataset_list

    def calculate_jaccard_sim(self):
        """

        :return:
        """
        sets_dict = dict()

        for source, words in self.data.items():
            sets_dict.update({str(source): set(words.split(" "))})

        datasets = self.init_dataset(sets_dict)

        for dataset in datasets:
            jaccard_sim = self.__calculate_jaccard_sim(dataset.body_tuple)
            dataset.calc_jaccard_sim = jaccard_sim

        data_handler.update_database_jaccard(datasets, self.database)

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

        datasets = self.init_dataset(sets_dict)

        for dataset in datasets:
            jaccard_sim = self.__estimate_jaccard_sim(dataset.body_tuple)
            dataset.est_jaccard_sim = jaccard_sim

        data_handler.update_database_jaccard(datasets, self.database)

        return

    @staticmethod
    def __calculate_jaccard_sim(body_tuple):
        """

        :return:
        """

        actual_jaccard = float(len(body_tuple[0].intersection(body_tuple[1]))) / float(len(body_tuple[0].union(body_tuple[1])))
        print("Actual Jaccard for data1 and data2 is", actual_jaccard)

        return actual_jaccard

    @staticmethod
    def __estimate_jaccard_sim(body_tuple):
        """

        :param minhash_sets_list:
        :return:
        """
        jaccard_sim = body_tuple[0].jaccard(body_tuple[1])
        print("Estimated Jaccard for data1 and data2 is", jaccard_sim)

        return jaccard_sim


class Dataset:
    def __init__(self, header1, header2, body1, body2):
        self.__header_tuple = "{}#{}".format(header1, header2)
        self.__body_tuple = (body1, body2)
        self.__est_jaccard_sim = None
        self.__calc_jaccard_sim = None
        self.__est_jaccard_time = None
        self.__calc_jaccard_time = None

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
        return {self.header_tuple: {"est_jaccard_sim": self.est_jaccard_sim,
                                    "est_jaccard_time": self.est_jaccard_time,
                                    "calc_jaccard_sim": self.calc_jaccard_sim,
                                    "calc_jaccard_time": self.calc_jaccard_time}}


if __name__ == "__main__":
    pass
    #m = JaccardSim("examples/output.source")
    #m = JaccardSim(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","examples","output.source"))

