import simhash
from datasketch import MinHash
import time
import ctypes
import re
import abc


class HashInterface:
    """
    This is the explanation class. All classes should inhert from it. All abc.abstractmethods need to be implemented in
    your child class. This ensures that all classes can reuse the input provides by the data_handler
    """
    @abc.abstractmethod
    def hash(self, text):
        """
        This is the hash function which is called from the main function. Put all hashing logic in here.
        If you want measurments seperate the parts you want to measure in sindle functions so that they are tracked by
        cprofile (which tracks the time for all function calls)

        :param text: the input from the data handlers text_dict
        :return: return the hash or the object on which you want to do the evaluation on
        """
        return

    @abc.abstractmethod
    def evaluate(self, args):
        """
        This is the evaluation method which takes whatever parameter you want as input and should yield a certain
        output about the similarities of different html documents.
        If the evaluation should be measured to use the same approach as above.

        :param args:
        :return: you can return something or write your results directly to disk
        """


class Simhash:
    def __init__(self, args):
        self.shingle_size = 9
        self.blocks = 8
        self.distance = 4

        for attr, value in args.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

    def hash(self, text):
        return self.__hash(self.__shingle(self.__tokenize(text), self.shingle_size))

    def evaluate(self, hashes):
        #print("Finding matches with block size of {} and distance of {}".format(self.blocks, self.distance))
        matches = self.__find_matches(hashes, self.blocks, self.distance)

        return matches

    @staticmethod
    def __hash(shingles):
        return simhash.compute([ctypes.c_ulong(hash(shingle)).value for shingle in shingles])

    @staticmethod
    def __tokenize(text):
        tokens = re.split("\s+", re.sub(r'[^\w\s]', '', text.lower()))
        return tokens

    @staticmethod
    def __shingle(token, shingle_size):
        return (' '.join(tokens) for tokens in simhash.shingle(token, shingle_size))

    @staticmethod
    def __find_matches(hashes, blocks, distance):
        return simhash.find_all(hashes, blocks, distance)


class Minhash:
    def hash(self, text):
        """
        Creates a min-hash for a given text by updating a MinHash with every word contained in the text.

        :param text: the string which should be hashed
        :return: MinHash()
        """
        m = MinHash()

        for line in text.split("\n"):
            m = self.__hash(m, line)

        return m

    def evaulate(self, text_dict, minhash_distance=0.9):
        """ This estimates the jaccard similarity between all entries in a set of min hashes. The results are stored
            in a special database.

        :return:
        """
        i = 0
        _time = 0
        matches = 0

        for offset1, hash1 in text_dict.items():
            i += 1
            j = 0
            for offset2, hash2 in text_dict.items():
                j += 1
                if j > i:
                    start = time.time()
                    estimated_jaccard_sim = self.__estimate_jaccard_sim(hash1.get("minhash"), hash2.get("minhash"))
                    _time = float(_time) + time.time() - start
                    if float(estimated_jaccard_sim) >= float(minhash_distance):
                        matches += 1

        if matches == 0:
            print("There were no documents with a similarity over {} found with minhash!".format(minhash_distance))
        else:
            print("Found {} document with a jaccard similarity of {} or higher".format(matches, minhash_distance))

        return _time

    @staticmethod
    def __hash(m, line):
        return m.update(line)

    @staticmethod
    def __estimate_jaccard_sim(minhash1, minhash2):
        """

        :param body_tuple:
        :return:
        """
        return minhash1.jaccard(minhash2)
