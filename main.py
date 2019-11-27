import os
import json
import argparse

from near_duplicate_detection import jaccard

FILE = os.path.dirname(os.path.abspath(__file__))  # Points to this folder (/home/something/something/text_mining/)
MODES = ["estimate_jaccard_sim", "calculate_jaccard_sim", "both_jaccard_sim"]  # Add your function call names here!


def __load_conf(config_name=os.path.join(FILE, "conf/example.conf")):
    """
    Simple config loader for a json formatted config file. Defaults to an example config.
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


# The basic concept is to call main.py with the -c parameter and give it a config file containing all values you need
# for the run. The Config parser will read all parameters from the command line and check if there is a -c parameter.
# If so it will load the config supplied with -c otherwise load the default config.
# Then if the config contains values that are also present via command line parameter it will be updated to the value
# submitted via command line.


parser = argparse.ArgumentParser()

parser.add_argument("-c", "--config", help="path of the config file (default: conf/example.conf)")
parser.add_argument("-m", "--mode", help="Choose between following modes: {}".format(MODES))
parser.add_argument("-i", "--input", help="path of an archive")
parser.add_argument("-o", "--output", help="path of the destination")
parser.add_argument("-db", "--database", help="path of the database (jaccard simularity)")

args = parser.parse_args()


if __name__ == "__main__":  # This is True is main.py was called from a command line

    if args.config:
        config = __load_conf(args.config)
    else:
        config = __load_conf()

    # If you add command line parameters add an entry here with "parameter_name": args.parameter_name
    updates = {"input": args.input, "output": args.output, "mode": args.mode, "config": args.config,
               "database": args.database}
    config = __update_config(config, updates)  # Updates the config with cmd parameters

    # Finally add a if clause "if config["mode"] == "your_mode_name": call_your_scripts_function()

    if config["mode"] in ["estimate_jaccard_sim", "calculate_jaccard_sim", "both_jaccard_sim"]:
        __Jaccard = jaccard.JaccardSim(config)
        __Jaccard.main()
