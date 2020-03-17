import simhash
from datasketch import MinHash
import ctypes
import re
import time


class Hash:
    """
    This is a general class. Due to required dynamic inheritance it will set a parent from the MODE_HASH_DICT and call
    functions of this class.
    """

    def __init__(self, mode, args):
        self.hash_time_dict = dict()
        self.find_time_dict = dict()

        self.__parent = MODE_HASH_DICT.get(mode)(args)

    def update_time_dicts(self):
        """
        This updates the time dicts of the Hash() class. Could be improved with dynamic inheritance.

        :return:
        """
        self.hash_time_dict = self.__parent.hash_time_dict
        self.find_time_dict = self.__parent.find_time_dict

    def hash(self, text):
        """
        This is the hash function which is called from the main function runners.

        :param text: the input from the data handler
        :return: bytes() - hashes text
        """
        return self.__parent.hash(text)

    def find_matches(self, hashes):
        """
        This functions finds matches for certain hashes and a defined distance measure.

        :param hashes:
        :return: list() - matched hashes as tuples
        """
        return self.__parent.find_matches(hashes)


class Simhash:
    def __init__(self, args):
        self.i = 0

        self.hash_time_dict = dict()
        self.find_time_dict = dict()

        self.shingle_size = args.get("shingle_size", 9)
        self.blocks = args.get("blocks", 8)
        self.distance = args.get("distance", 4)

    def hash(self, text):
        """
        This takes a text as argument and hashes it using the simhash algorithm

        :param text: str()
        :return: bytes() - hash
        """
        self.i += 1

        start = time.time()

        h = self.__hash(self.__shingle(self.__tokenize(text), self.shingle_size))

        self.hash_time_dict.update({self.i: (time.time() - start)})

        return h

    def find_matches(self, hashes):
        """
        This finds hashes that have a distance lower than self.distance. It'll return a list of tuples of matches.

        :param hashes: list(bytes())
        :return: list(tuple())
        """
        return self.__find_matches(hashes, self.blocks, self.distance)

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

    def __find_matches(self, hashes, blocks, distance):
        start = time.time()
        m = simhash.find_all(hashes, blocks, distance)
        average_time = (time.time() - start) / len(hashes)

        for i in range(len(hashes)):
            self.find_time_dict.update({i: average_time})

        return m


class Minhash:
    def __init__(self, args):
        self.i = 0

        self.hash_time_dict = dict()
        self.find_time_dict = dict()

        self.minhash_distance = float(args.get("jaccard_sim", 0.7))

    def hash(self, text):
        """
        Creates a min-hash for a given text by updating a MinHash with every word contained in the text.

        :param text: the string which should be hashed
        :return: MinHash()
        """
        self.i += 1

        m = MinHash()
        start = time.time()

        for line in text.split("\n"):
            self.__hash(m, line.encode('utf-8'))

        self.hash_time_dict.update({self.i: (time.time() - start)})

        return m

    def find_matches(self, hashes):
        """ This estimates the jaccard similarity between all entries in a set of min hashes. The results are stored
            in a special database.

        :return:
        """
        matches = list()
        hashes = list(hashes)

        for i in range(len(hashes)):
            start = time.time()
            for j in range(len(hashes)):

                if j > i:
                    estimated_jaccard_sim = self.__estimate_jaccard_sim(hashes[i], hashes[j])

                    if float(estimated_jaccard_sim) >= float(self.minhash_distance):
                        matches.append((hashes[i], hashes[j]))

            self.find_time_dict.update({i: (time.time() - start)})
            self.i += 1

        return matches

    @staticmethod
    def __hash(m, line):
        m.update(line)

    @staticmethod
    def __estimate_jaccard_sim(minhash1, minhash2):
        return minhash1.jaccard(minhash2)


class Justushash:
    """
    Justushash implements the simhash idea in our own algorithm. It is way slower than simhash but gives a good insight
    on how the algorithm works.
    """
    def __init__(self, args):
        self.hash_time = 0
        self.find_time = 0
        self.shingle_size = 9
        self.blocks = 8
        self.distance = 4

    def hash(self, text):
        start = time.time()
        shingles = self.__shingle(text, self.shingle_size)
        hash = self.__hash(shingles)
        self.hash_time += time.time() - start
        return self.__bitShift(hash)

    def find_matches(self, hashes):
        start = time.time()
        matches = list()
        sorted_hashes = self.__sort(hashes)
        # print(similarity)
        for i in range(0, len(sorted_hashes)):
            for j in range(1, len(sorted_hashes)):
                if self.__hamming(sorted_hashes[i], sorted_hashes[j]) <= self.distance:
                    matches.append((sorted_hashes[i], sorted_hashes[j]))
                else:
                    break
        self.find_time += time.time() - start
        return matches

    @staticmethod
    def __shingle(text, shingle_size):
        shingles = list()
        for i in range(0, len(text)):
            shingles.append(text[i:i+shingle_size])
        return shingles

    @staticmethod
    def __hash(shingles):
        sim = [0 for _ in range(64)]

        i = 0
        for sh in shingles:
            # print(sh)
            h = bin(hash(sh))
            # print(h)

            if h.startswith("0"):
                # print("-------------------------------------------")
                h = h[2:len(h)]
                if len(h) < 64:
                    h = (64 - len(h)) * '0' + h
                    # print(h)

            if h.startswith("-"):
                # print("-------------------------------------------")
                h = h[3:len(h)]
                if len(h) < 64:
                    h = (64 - len(h)) * '0' + h
                    # print(h)

            h = str(h)

            # sim = split(sim)

            # print("sim:")
            # print(sim)

            for i in range(0, len(h)):
                # print("i " + str(i))
                if h[i] == "1":
                    # print("simadd")
                    # print(sim[i])
                    sim.insert(i, str(int(sim[i]) + 1))
                    sim.pop(i + 1)
                    # sim = sim[i-abs(i-1):i+1] + str(int(sim[i]) + 1) + sim[i+1:]

                if h[i] == "0":
                    # print("simdiv")
                    # print(sim[i])
                    sim.insert(i, str(int(sim[i]) - 1))
                    sim.pop(i + 1)
                    # sim = sim[i-abs(i-1):i+1] + str(int(sim[i]) - 1) + sim[i+1:]


                    # print(sim)

        for i in range(0, len(sim)):
            if int(sim[i]) <= 0:
                sim.insert(i, "0")
                sim.pop(i + 1)

            if int(sim[i]) > 0:
                sim.insert(i, "1")
                sim.pop(i + 1)

        h = ""
        for c in sim:
            h += c
        # print(h)

        del shingles[:]

        return h

    @staticmethod
    def __bitShift(h):
        simH = h[0:4]
        sim = h[4:] + simH
        return sim

    @staticmethod
    def __sort(hashes):
        for i in range(0, len(hashes)):
            for j in range(1, len(hashes)):
                if hashes[j] < hashes[i]:
                    hashes[j], hashes[i] = hashes[i], hashes[j]

        return hashes

    @staticmethod
    def __hamming(bin1, bin2):
        ham = 0
        # print(bin1 + "---" + bin2)
        for i in range(0, len(bin1)):
            if bin1[i] != bin2[i]:
                ham += 1
        return ham


MODE_HASH_DICT = {"simhash": Simhash, "minhash": Minhash, "justushash": Justushash}
