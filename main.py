import os
import sys
import json
import argparse
import time

from lib.data_handler import DataHandler
from near_duplicate_detection.hasher import Simhash, Minhash

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
        print("Config:")
        for key, value in conf_dict.items():
            print("    {}: {}".format(key, value))

            # This makes sure that values that are 'True' in the config are also set to True in the code
            if value == "true" or value =="False":
                conf_dict[key] = BOOL_DICT[value]
            else:
                conf_dict[key] = value

        print("Successfully loaded config from /home/robby/git/text_mining/conf/example.conf!\n".format(_config))

        return conf_dict


parser = argparse.ArgumentParser()  # This is the cmd-line parser

parser.add_argument("-c", "--config", help="path of the config file (default: conf/example.conf)")

args = parser.parse_args()

if __name__ == "__main__":  # This is True if main.py was called from a command line
    if args.config:
        config = __load_conf(args.config)
    else:
        config = __load_conf()

    if not config.get("source"):
        raise FileNotFoundError("Ńo source file in config found!")

    source = config.pop("source")

    # Init the DataHandler
    print("Reading in the data source ...")
    #data = DataHandler(source)
    #offset_text_dict = data.text_dict
    with open("data/text_entries", "r") as file:
        offset_text_dict = json.load(file)
    print("Finished reading {} records!\n".format(len(offset_text_dict)))

    for run, values in config.items():
        hash_list = list()
        hash_offset_dict = dict()

        print("Starting run {} with following values:\n{}".format(run, values))

        if not values.get("mode"):
            raise ModuleNotFoundError("Entry mode was not found in the config file!")
        elif values.get("mode") == "simhash":
            hasher = Simhash(values.get("additional_parameter"))

        print("Calculating hashes ...")

        #for offset, text in offset_text_dict.items():
        #    hash_offset_dict.update({hasher.hash(text): offset})
        with open("data/simhash_hashes.json", "r") as file:
            offset_hash_dict = json.load(file)
            for key, value in offset_hash_dict.items():
                hash_offset_dict.update({value: key})

        print("Finding matching pairs ...")

        matches = hasher.evaluate(hash_offset_dict.keys())
        print("Found {} matches!\n\n".format(len(matches)))

        #i = 0
        #for match in matches:
        #    i += 1
        #    offset_1 = hash_offset_dict.get(match[0])
        #    offset_2 = hash_offset_dict.get(match[1])

        #    with open("data/{}_{}".format(offset_1, offset_2), "w") as file:
        #        file.write("{}\n#####\n{}".format(offset_text_dict.get(offset_1), offset_text_dict.get(offset_2)))

        #    if i == 100:
        #        break



