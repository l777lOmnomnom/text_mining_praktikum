import os
import json
import argparse

from near_duplicate_detection import minhash

FILE = os.path.dirname(os.path.abspath(__file__))  # Points to this folder (/home/something/something/text_mining/)
MODES = {"minhash": minhash.Minhash}

"""
There are 2 ways of starting injecting your variables into the scripts. Both will create a dictonary with your values as
config_dict = {"config_entry_name": value} which should be added to your class call.

command_line arguments
    - add your argument to the argument parser ('parser.add_argument("-i", "--input", help="path of an archive")')
      (you can use already existing parameters without changing anything, they are available via config.get("parameter")
    - add your argument to the update at the bottom (this is mandatory!)

config arguments
    - add a config file in conf
    - add your parameters to the config file (see conf/example.conf)
    - start main.py with the -c parameter or edit the example.conf which is the default config
    
Finally add your class to MODES on the top of the file. If your config or command line parameter includes "mode" and 
mode is an entry in the MODES dict the class will be automatically called with the config dict.
"""


def __load_conf(config_name=os.path.join(FILE, "conf/example.conf")):
    """

    :param config_name:
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


if __name__ == "__main__":  # This is True is main.py was called from a command line

    #if args.config:
    #    config = __load_conf(args.config)
    #else:
    config = __load_conf()

    # If you add command line parameters add an entry here with "parameter_name": args.parameter_name
    #updates = {"source": args.input, "archive": args.output, "database": args.database}

    #config = __update_config(config, updates)  # Updates the config with cmd parameters

    # Finally add your class in the dictonary at the top (MODES) and add the key as mode
    MODES.get(config.get("mode"))(config).main()
