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


parser = argparse.ArgumentParser()

# Mandatory Parameters which should not be put into the config as they are only required here!
parser.add_argument("-c", "--config", help="path of the config file (default: conf/example.conf)")
parser.add_argument("-m", "--mode", help="Choose between following modes: {}".format(MODES))

# Files to operate on
parser.add_argument("-i", "--input", help="path of an archive")
parser.add_argument("-o", "--output", help="path of the destination")
parser.add_argument("-db", "--database", help="path of the database (jaccard simularity)")


# Optional Parameters and parameters that should update the config
# ...

args = parser.parse_args()


if __name__ == "__main__":  # This is True is main.py was called from a command line

    # The args parser takes command line arguments which can be passed using the args container.
    # You can also use a config file to store the parameters and just use "python3 main.py -c path/to/your/config" to
    # start processing . Nonetheless, parameters from the command line overwrite config entries!

    if args.config:
        config = __load_conf(args.config)
    else:
        config = __load_conf()

    updates = {"input": args.input, "output": args.output, "mode": args.mode, "config": args.config,
               "database": args.database}
    config = __update_config(config, updates)

    # Finally add a if clause "if config["mode"] == "your_mode_name": call_your_scripts_function()

    if config["mode"] in ["estimate_jaccard_sim", "calculate_jaccard_sim", "both_jaccard_sim"]:
        __class = jaccard.JaccardSim(config)
        if config["mode"] == "both_jaccard_sim":
            getattr(__class, "estimate_jaccard_sim")()
            getattr(__class, "calculate_jaccard_sim")()
        #getattr(__class, config["mode"])()
