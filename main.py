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
            if key == "source":
                value = "/home/robby/git/text_mining/data/archives/de_web_2019.01000.warc.gz"
            print("Loaded config entry {} with value {}".format(key, value))
            if value == "true" or value =="False":
                conf_dict[key] = BOOL_DICT[value]

        print("\nSuccessfully loaded config from /home/robby/git/text_mining/conf/example.conf!".format(_config))
        print("________________________________________\n")
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
                                        100)

    print("Calculating similarieties using Minhash took an additional {} seconds".format(
        hasher.Minhash().main(hash_db)))
    print("Calculating similarieties using Simhash took an additional {} seconds".format(
        hasher.Simhash().main(hash_db)))

    print("________________________________________\n")

    hash_db = DataHandler().get_hash_db(config.get("source"),
                                        config.get("simhash"),
                                        config.get("minhash"),
                                        1000)

    print("Calculating similarieties using Minhash took an additional {} seconds".format(
        hasher.Minhash().main(hash_db)))
    print("Calculating similarieties using Simhash took an additional {} seconds".format(
        hasher.Simhash().main(hash_db)))

    print("________________________________________\n")

    hash_db = DataHandler().get_hash_db(config.get("source"),
                                        config.get("simhash"),
                                        config.get("minhash"),
                                        5000)

    print("Calculating similarieties using Minhash took an additional {} seconds".format(
        hasher.Minhash().main(hash_db)))
    print("Calculating similarieties using Simhash took an additional {} seconds".format(
        hasher.Simhash().main(hash_db)))
