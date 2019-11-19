import data_handler
from datasketch import MinHash


class Minhash:
    def __init__(self, input=None):
        #self.archive = data_handler.extract_archive(os.path.join(os.path.dirname(os.path.abspath(__file__)),
        #                                            'resources',
        #                                            'de_web_2019.01000.warc.gz'))

        self.data1 = data_handler.get_data("/tmp/output.source", 10)
        self.data2 = data_handler.get_data("/tmp/output.source", 10, 10)

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
    m = Minhash()

