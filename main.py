import sys
import json
import argparse

from near_duplicate_detection.runner import Runner

# This is command line parser, its quite self explanatory
parser = argparse.ArgumentParser()  # This is the cmd-line parser
parser.add_argument("-c", "--config", help="path of the config file (default: conf/example.conf)")

args = parser.parse_args()
bool_map = {"True": True, "False": False}  # Helps to read in config file


def __load_conf(_config="conf/example.conf"):
    """ This is the first function to be called. It will load all config entries from the config file.
    You can specify a config by calling this script with -c /path/to/conf.file
    All values loaded from the config are stored in a dictionary and are handed to the class you specified in mode

    :param _config: The path to the config file
    :return:
    """
    try:
        print(_config)
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
                conf_dict[key] = bool_map[value]
            else:
                conf_dict[key] = value

        return conf_dict


if __name__ == "__main__":  # This is True if main.py was called from a command line
    if args.config:
        config = __load_conf(args.config)
    else:
        config = __load_conf()

    for run, values in config.items():
        runner = Runner(run, values)

        runner.create_offset_hash_map()
        runner.find_similar_hashes()
        runner.dump()
