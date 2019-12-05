#import pandas as pd
from warcio import ArchiveIterator
import simhash
import re
import ctypes
import json
import time
from bs4 import BeautifulSoup
from lib import data_handler


class Simhash:
    def __init__(self, config):
        self.__elements = config.get("elements", 1000)
        self.__offset = config.get("offset", 0)
        self.__all = config.get("all", False)
        self.__tracker = 0
        self.__input = config.get("input")
        self.__output = config.get("output")
        self.__database = config.get("database")

        self.data_handler = data_handler.DataHandlerSimHash()

        # Currently limited of a small subset of data
        self.__data = dict()

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

    @property
    def input(self):
        return self.__input

    @input.setter
    def input(self, __i):
        self.__input = __i

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, __o):
        self.__output = __o

    @property
    def database(self):
        return self.__database

    @database.setter
    def database(self, __d):
        self.__database = __d

    def main(self):
        start_time = time.time()

        hashes, data_dict = self.data_handler.get_hash_list(self.input, self.elements)

        print("--- %s seconds --- End of Hashing" % (time.time() - start_time))

        matches = simhash.find_all(hashes, 8, 6)

        print("--- %s seconds --- End of finding similar hashes" % (time.time() - start_time))

        with open('/tmp/similiar_data.txt', 'w') as file:
                file.write('\n'.join('%s %s' % x for x in matches))

        print("--- %s seconds ---" % (time.time() - start_time))