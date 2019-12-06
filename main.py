import os
import json
import argparse

from near_duplicate_detection import min_hash, sim_hash

FILE = os.path.dirname(os.path.abspath(__file__))  # Points to this folder (/home/something/something/text_mining/)


def __load_conf(config=os.path.join(FILE, "conf/example.conf")):
    """ This is the first function to be called. It will load all config entries from the config file.
    You can specify a config by calling this script with -c /path/to/conf.file
    All values loaded from the config are stored in a dictionary and are handed to the class you specified in MODES

    :param config: The path to the config file
    :return:
    """
    try:
        with open(config, "r") as conf:
            conf_dict = json.load(conf)
    except IOError as err:
        print("Failed to load config: {}".format(err))
    else:
        print("Successfuly loaded config from: {}".format(config))
        return conf_dict


parser = argparse.ArgumentParser()  # This is the cmd-line parser
parser.add_argument("-c", "--config", help="path of the config file (default: conf/example.conf)")
args = parser.parse_args()


if __name__ == "__main__":  # This is True if main.py was called from a command line
    if args.config:
        config = __load_conf(args.config)
    else:
        config = __load_conf()

    # This is the part where you start your script. Add a new elif clause with your mode name (choose one) and call your
    # script in the body of your clause.
    if not config.get('mode'):
        raise NotImplemented("No mode specified. This is not implemented!")

    elif config.get('mode') == "update_hash_db":
        # This will update the hash database with new entries for minhash and simhash
        # Attention: this will always calculate the hashes for all source data and then update the database
        # TODO: Only calculate the hashes of entries not aready collected
        sim_hash.Simhash(config).update_hash_db()
        min_hash.Minhash(config).update_hash_db()

    elif config.get("mode") == "update_min_hash_jaccard_matrix":
        pass

    elif config.get("mode") == "simhash":
        sim_hash.Simhash(config)


# TO BE IMPLEMENTED
# This ius a function that can take the command line arguments and update the config with them
"""
def __update_config(conf_dict, values):
    for key, value in values.items():
        if value is not None:
            conf_dict.update({key: value})

    return conf_dict
"""