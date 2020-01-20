import os
import sys
import json
import argparse
import subprocess

from lib.data_handler import DataHandler
from near_duplicate_detection.hasher import Simhash, Minhash, Justushash

FILE = os.path.dirname(os.path.abspath(__file__))  # Points to this folder (/home/something/something/text_mining/)
BOOL_DICT = {"True": True, "False": False}


def __store_diff(output_path, _offset_text_dict, offset_a, offset_b):
    with open(os.path.join(output_path, "a"), "w") as a:
        a.write(_offset_text_dict.get(str(offset_a)))

    with open(os.path.join(output_path, "b"), "w") as b:
        b.write(_offset_text_dict.get(str(offset_b)))

    diff = os.system("diff {} {}".format(os.path.join(FILE, output_path, "a"),
                                         os.path.join(FILE, output_path, "b")))

    return diff


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
        print("Config:\n")
        for key, value in conf_dict.items():
            print("    {}: {}".format(key, value))

            # This makes sure that values that are 'True' in the config are also set to True in the code
            if value == "true" or value =="False":
                conf_dict[key] = BOOL_DICT[value]
            else:
                conf_dict[key] = value

        print("\nSuccessfully loaded config from /home/robby/git/text_mining/conf/example.conf!\n".format(_config))

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
    data = DataHandler(source, config.get("max_elements"))
    offset_text_dict = data.text_dict

    for run, values in config.items():
        hash_list = list()  # Hash list for use in the evaluate function
        hash_offset_dict = dict()  # A dict containing hash: offset

        print("\nStarting run {} with following values:\n{}".format(run, values))

        if values.get("mode") == "simhash":
            hasher = Simhash(values.get("additional_parameter"))
        elif values.get("mode") == "justushash":
            hasher = Justushash(values.get("additional_parameter"))
        else:
            raise ModuleNotFoundError("Entry mode was not found in the config file!")

        print("\nCalculating hashes ...".format(len(offset_text_dict)))
        if os.path.isfile("{}_hashes.json".format(source.split(".")[0])):
            with open("{}_hashes.json".format(source.split(".")[0]), "r") as file:
                hash_offset_dict = json.load(file)
        else:
            for offset, text in offset_text_dict.items():
                hash_offset_dict.update({hasher.hash(text): offset})
            with open("{}_hashes.json".format(source.split(".")[0]), "w") as file:
                json.dump(hash_offset_dict, file)

        print("Searching matches ...")
        matches = hasher.evaluate(list(hash_offset_dict.keys()))
        print("Found {} matches!\n\n".format(len(matches)))

        print("Creating a results folder in {} and storing all results there.".format(source.split(".")[0]))
        output = source.split(".")[0]
        if not os.path.isdir(output):
            os.mkdir(output)

        i = 0
        for match in matches:
            i += 1

            # This makes evaluation easier as all files are ordered by their smallest offset
            # if match[0] > match[1]:
            #    match[0], match[1] = match[1], match[0]

            offset_a, offset_b = hash_offset_dict.get(match[0]), hash_offset_dict.get(match[1])
            with open(os.path.join(output, "{}_{}_{}".format(offset_a, offset_b, run)), "w") as file:
                infos = "Config:\n{}".format(config)
                text_a = "Offset: {}\nHash: {}\nLength: {}\n\n{}".format(offset_a,
                                                                         match[0],
                                                                         len(offset_text_dict.get(offset_a)),
                                                                         offset_text_dict.get(offset_a))
                text_b = "Offset: {}\nHash: {}\nLength: {}\n\n{}".format(offset_b,
                                                                         match[1],
                                                                         len(offset_text_dict.get(offset_a)),  # noqa
                                                                         offset_text_dict.get(offset_a))  # noqa

                file.write("{}\n\n{}\n\n{}\n\n{}".format(infos, text_a, "#"*25, text_b))

            # This should save the diff but doesn't work ...
            # with open(os.path.join(output, "{}_{}_diff".format(offset_a, offset_b)), "w") as file:
            #    file.write(__store_diff(output, offset_text_dict, offset_a, offset_b))

            if i == 3:
                break
