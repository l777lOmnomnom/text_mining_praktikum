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
    def estimate_jaccard_sim(self, hash_db, minhash_distance=0.9):
        """ This estimates the jaccard similarity between all entries in a set of min hashes. The results are stored
            in a special database.

        :return:
        """
        i = 0
        _time = 0
        matches = 0

        for offset1, hash1 in hash_db.items():
            i += 1
            j = 0
            for offset2, hash2 in hash_db.items():
                j += 1
                if j > i:
                    start = time.time()
                    estimated_jaccard_sim = self.__estimate_jaccard_sim(hash1.get("minhash"), hash2.get("minhash"))
                    _time = float(_time) + time.time() - start
                    if float(estimated_jaccard_sim) > float(minhash_distance):
                        matches += 1

        if matches == 0:
            print("There were no documents with a similarity over {} found with minhash!".format(minhash_distance))
        else:
            print("Found {} document with a jaccard similarity of {} or higher".format(matches, minhash_distance))

        return _time

    @staticmethod
    def __estimate_jaccard_sim(minhash1, minhash2):
        """

        :param body_tuple:
        :return:
        """
        return minhash1.jaccard(minhash2)
