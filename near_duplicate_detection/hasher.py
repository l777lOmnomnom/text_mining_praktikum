#import pandas as pd
from warcio import ArchiveIterator
import simhash
import re
import ctypes
import json
import time
from bs4 import BeautifulSoup
from lib import data_handler
import os
import time
import sys


class Simhash:

    def main(self):
        start_time = time.time()

        #print("Calculating the Simhash for {} elements took {} seconds".format(len(data), self.data_handler.time))

        #matches = simhash.find_all(hashes, 8, 6)

        #print("--- %s seconds --- End of finding similar hashes" % (time.time() - start_time))

        #with open('/tmp/similiar_data.txt', 'w') as file:
        #        file.write('\n'.join('%s %s' % x for x in matches))

        #print("--- %s seconds ---" % (time.time() - start_time))


class Minhash:
    def estimate_jaccard_sim(self, hash_db):
        """ This estimates the jaccard similarity between all entries in a set of min hashes. The results are stored
            in a special database.

        :return:
        """
        est_dict = dict()
        i = 0
        _time = 0

        for offset1, hash1 in hash_db.items():
            i += 1
            j = 0
            for offset2, hash2 in hash_db.items():
                j += 1
                if j > i:
                    start = time.time()
                    estimated_jaccard_sim = self.__estimate_jaccard_sim(hash1.get("minhash"), hash2.get("minhash"))
                    _time = float(_time) + time.time() - start

        return _time

    @staticmethod
    def __estimate_jaccard_sim(minhash1, minhash2):
        """

        :param body_tuple:
        :return:
        """
        return minhash1.jaccard(minhash2)
