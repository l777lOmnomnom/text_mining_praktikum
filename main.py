import os
import sys
import json
import argparse

from near_duplicate_detection import hasher
from lib.data_handler import DataHandler

FILE = os.path.dirname(os.path.abspath(__file__))  # Points to this folder (/home/something/something/text_mining/)
BOOL_DICT = {"True": True, "False": False}


def __load_conf(_config=os.path.join(FILE, "conf/example.conf")):
    """ This is the first function to be called. It will load all config entries from the config file.
    You can specify a config by calling this script with -c /path/to/conf.file
    All values loaded from the config are stored in a dictionary and are handed to the class you specified in MODES

    :param _config: The path to the config file
    :return:
    """
    try:
        with open(_config, "r") as conf:
            conf_dict = json.load(conf)
    except IOError as err:
        print("Failed to load config: {}".format(err))
        sys.exit(1)
    else:
        # This makes sure that values that are 'True' in the config are also set to True in the code
        for key, value in conf_dict.items():
            print("Loaded config entry {} with value {}".format(key, value))
            if BOOL_DICT.get(value):
                conf_dict[key] = BOOL_DICT[value]

        print("Successfully loaded config from {}!\n ________________________________________\n".format(_config))

        return conf_dict


parser = argparse.ArgumentParser()  # This is the cmd-line parser

parser.add_argument("-c", "--config", help="path of the config file (default: conf/example.conf)")

args = parser.parse_args()


if __name__ == "__main__":  # This is True if main.py was called from a command line
    if args.config:
        config = __load_conf(args.config)
    else:
        config = __load_conf()

    # Example Calls
    hash_db = DataHandler().get_hash_db(config.get("source"),
                                        config.get("simhash"),
                                        config.get("minhash"),
                                        config.get("elements"))

    time = hasher.Minhash().estimate_jaccard_sim(hash_db, config.get("minhash_distance"))

    print("Estimating Jaccard Similarieties using Minhash took an additional {} seconds\n".format(time))

    hash_db = DataHandler().get_hash_db(config.get("source"),
                                        config.get("simhash"),
                                        config.get("minhash"),
                                        100)

    time = hasher.Minhash().estimate_jaccard_sim(hash_db, config.get("minhash_distance"))

    print("Estimating Jaccard Similarieties using Minhash took an additional {} seconds\n".format(time))

    hash_db = DataHandler().get_hash_db(config.get("source"),
                                        config.get("simhash"),
                                        config.get("minhash"),
                                        1000)

    print("Estimating Jaccard Similarieties using Minhash took an additional {} seconds\n".format(time))

    time = hasher.Minhash().estimate_jaccard_sim(hash_db, config.get("minhash_distance"))
