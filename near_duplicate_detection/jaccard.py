from datasketch import MinHash

from lib import data_handler


class Minhash:
    def __init__(self, input_file=None):
        self.__input_file = input_file

        self.__data = data_handler.read_source(input_file)

        self.build_jaccard_database()

    @property
    def data(self):
        return self.__data

    def build_jaccard_database(self):
        minhash_sets_list, jaccard_sets_list = list(), list()
        for source, words in self.data.items():

            print("Current source: {}".format(source))
            m = MinHash()
            for word in words:
                m.update(word.encode('utf8'))

            minhash_sets_list.append(m)
            jaccard_sets_list.append(set(words.split(" ")))

        for index, s in enumerate(minhash_sets_list):
            for i in range(index + 1, len(minhash_sets_list)):
                jaccard_sim = s.jaccard(minhash_sets_list[i])
                print("Estimated Jaccard for data1 and data2 is", jaccard_sim)

        for index, s in enumerate(jaccard_sets_list):
            for i in range(index + 1, len(jaccard_sets_list)):
                actual_jaccard = float(len(s.intersection(jaccard_sets_list[i]))) / float(len(s.union(jaccard_sets_list[i])))
                print("Actual Jaccard for data1 and data2 is", actual_jaccard)


    @staticmethod
    def update_minhash_set(data, minhash_set=None):
        """
        This updates a minhash set. If no set is given, a new one will be created and returned. Otherwise the given
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
        """
        This calculates the jaccard similarity between set1 and set2.

        :param set1:
        :param set2:
        :return:
        """
        s1, s2 = set(set1), set(set2)
        return float(len(s1.intersection(s2)))/float(len(s1.union(s2)))


if __name__ == "__main__":
    m = Minhash("examples/output.source")

