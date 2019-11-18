from datasketch import MinHash


def update_minhash_set(data, minhash_set=None):
    """ This updates a minhash set. If no set is given, a new one will be created and returned. Otherwise the given
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


def calc_jaccard_similarity(set1, set2):
    """ This calculates the jaccard similarity between set1 and set2.

    :param set1:
    :param set2:
    :return:
    """
    s1, s2 = set(set1), set(set2)
    return float(len(s1.intersection(s2)))/float(len(s1.union(s2)))



