import os
import json
import argparse

from near_duplicate_detection import min_hash, sim_hash

FILE = os.path.dirname(os.path.abspath(__file__))  # Points to this folder (/home/something/something/text_mining/)
MODES = {"minhash": min_hash.Minhash, "simhash": sim_hash.Simhash}


def __load_conf(config_name=os.path.join(FILE, "conf/example.conf")):
    """ This is the first function to be called. It will load all config entries from the config file.
    You can specify a config by calling this script with -c /path/to/conf.file
    All values loaded from the config are stored in a dictonary and are handed to the class you specified in MODES

    :param config_name: The path to the config file
    :return:
    """
    try:
        with open(config_name, "r") as conf:
            conf_dict = json.load(conf)
    except IOError as err:
        print("Failed to load config: {}".format(err))
    else:
        return conf_dict


def __update_config(conf_dict, values):
    """
    This overwrites all config parameters if a corresponding command line input exists

    :param conf_dict:
    :param values:
    :return:
    """
    for key, value in values.items():
        if value is not None:
            conf_dict.update({key: value})

    return conf_dict


parser = argparse.ArgumentParser()

parser.add_argument("-c", "--config", help="path of the config file (default: conf/example.conf)")
parser.add_argument("-s", "--source", help="path of an .source file")
parser.add_argument("-a", "--archive", help="path of the archive")
parser.add_argument("-db", "--database", help="path of the database directory")

args = parser.parse_args()


if __name__ == "__main__":  # This is True if main.py was called from a command line

    if args.config:
        config = __load_conf(args.config)
    else:
        config = __load_conf()

    # If you add command line parameters add an entry here with "parameter_name": args.parameter_name
    # This will then be added to the config
    #updates = {"database": args.database}

    #config = __update_config(config, updates)  # Updates the config with cmd parameters

    # Add your class in the dictonary at the top (MODES) and add the key as mode in our config (see example.conf)
    MODES.get(config.get("mode"))(config).main()
