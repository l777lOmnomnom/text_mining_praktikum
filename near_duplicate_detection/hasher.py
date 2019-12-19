import simhash
import time


class Simhash:

    def main(self, hash_db, blocks=8, distance=6):

        hashes = list()
        for _hash in hash_db.values():
            hashes.append(_hash.get("simhash"))

        start_time = time.time()
        matches = simhash.find_all(hashes, blocks, distance)
        print(matches)
        if len(matches) == 0:
            print("\nThere were no documents with a bit difference under {} found with simhash!".format(distance))
        else:
            print("Found {} document with a bit difference under {}\n".format(len(matches), distance))

        return time.time() - start_time


class Minhash:
    def main(self, hash_db, minhash_distance=0.9):
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
            print("\nThere were no documents with a similarity over {} found with minhash!".format(minhash_distance))
        else:
            print("Found {} document with a jaccard similarity of {} or higher\n".format(matches, minhash_distance))

        return _time

    @staticmethod
    def __estimate_jaccard_sim(minhash1, minhash2):
        """

        :param body_tuple:
        :return:
        """
        return minhash1.jaccard(minhash2)
