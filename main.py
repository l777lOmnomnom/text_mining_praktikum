import os
import sys
import json
import argparse
import cProfile

from lib.data_handler import DataHandler
from near_duplicate_detection.hasher import Simhash, Minhash, Justushash

FILE = os.path.dirname(os.path.abspath(__file__))  # Points to this folder (/home/something/something/text_mining/)


parser = argparse.ArgumentParser()  # This is the cmd-line parser
parser.add_argument("-c", "--config", help="path of the config file (default: conf/example.conf)")
args = parser.parse_args()


def __load_conf(_config=os.path.join(FILE, "conf/example.conf")):
    """ This is the first function to be called. It will load all config entries from the config file.
    You can specify a config by calling this script with -c /path/to/conf.file
    All values loaded from the config are stored in a dictionary and are handed to the class you specified in mode

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

        return conf_dict





def __store_diff(output_path, _offset_text_dict, offset_a, offset_b):
    """
    Doesn't work :/

    :param output_path:
    :param _offset_text_dict:
    :param offset_a:
    :param offset_b:
    :return:
    """
    with open(os.path.join(output_path, "a"), "w") as a:
        a.write(_offset_text_dict.get(str(offset_a)))

    with open(os.path.join(output_path, "b"), "w") as b:
        b.write(_offset_text_dict.get(str(offset_b)))

    diff = os.system("diff {} {}".format(os.path.join(FILE, output_path, "a"),
                                         os.path.join(FILE, output_path, "b")))

    return diff


def main():
    if args.config:
        config = __load_conf(args.config)
    else:
        config = __load_conf()

    if not config.get("source"):
        raise FileNotFoundError("Ńo source file in config found!")

    # Extract source from the config
    source = config.pop("source")

    # Init the DataHandler
    print("Reading in the data source ...")
    data = DataHandler(source, config.get("max_elements"))

    offset_text_dict = data.text_dict  # This is the dict which maps offsets to their text

    for run, values in config.items():
        if values.get("max_elements"):
            i = int(values.get("max_elements")) + 1
            while i > values.get("max_elements"):
                offset_text_dict.popitem()
                i = len(offset_text_dict)
        print("Reduced elements to {}".format(len(offset_text_dict)))

        offset_hash_dict = dict()  # This will be the dict which maps offsets to their hashes

        print("\nStarting run {} with following values:\n{}".format(run, values))

        # Get the hash class
        if values.get("mode") == "simhash":
            hasher = Simhash(values.get("additional_parameter"))
        elif values.get("mode") == "justushash":
            hasher = Justushash(values.get("additional_parameter"))
        elif values.get("mode") == "minhash":
            hasher = Minhash(values.get("additional_parameter"))
        else:
            raise ModuleNotFoundError("Entry mode was not found in the config file!")

        # If you want to sped up minash you can your this but enable and format the for clause bellow
        if os.path.isfile("{}_hashes.json".format(source.split(".")[0])) and values.get("mode") == "simhash":
            print("\nLoading hashes from file ...".format(len(offset_text_dict)))
            with open("{}_hashes.json".format(source.split(".")[0]), "r") as file:
                offset_hash_dict = json.load(file)
        else:
            print("\nCalculating hashes ...".format(len(offset_text_dict)))
            for offset, text in offset_text_dict.items():
                offset_hash_dict.update({offset: hasher.hash(text)})
                if len(offset_hash_dict) == 1000:
                    break
                if values.get("mode") == "simhash":
                    with open("{}_hashes.json".format(source.split(".")[0]), "w") as file:
                        json.dump(offset_hash_dict, file)

        # Searches for similar documents and formats them to a offset tuple list
        print("Searching for similar documents ...")
        hash_list = list(offset_hash_dict.values())

        matched_offsets_list = __to_offset_list(hasher.evaluate(hash_list), offset_hash_dict)

        print("Found {} matches!\n".format(len(matched_offsets_list)))

        # Create an output dir in the sources name without all extensionens + _mode (e.g. simhash, minhash, etc)
        output_dir = "{}".format(source.split(".")[0])
        print("Creating a results folder in {} and storing all results there.".format(output_dir))
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

        i = 0

        # This iterates though all matches tuples and stores different stuff
        for match in matched_offsets_list:
            i += 1

            if int(match[0] > match[1]):
                offset_a = match[1]
                offset_b = match[0]
            else:
                offset_a = match[0]
                offset_b = match[1]

            # Create an output file in the output_dir + _offset_a_offset_b_run
            with open(os.path.join(output_dir, "{}_{}_{}_{}".format(offset_a, offset_b, run, values.get("mode"))), "w") as file:
                infos = "Config:\n{}".format(config)
                text_a = "Offset: {}\nHash: {}\nLength: {}\n\n{}".format(offset_a,
                                                                         offset_hash_dict.get(offset_a),
                                                                         len(offset_text_dict.get(offset_a)),
                                                                         offset_text_dict.get(offset_a))

                text_b = "Offset: {}\nHash: {}\nLength: {}\n\n{}".format(offset_b,
                                                                         offset_hash_dict.get(offset_b),
                                                                         len(offset_text_dict.get(offset_b)),  # noqa
                                                                         offset_text_dict.get(offset_b))  # noqa

                file.write("{}\n\n{}\n\n{}\n\n{}".format(infos, text_a, "#"*25, text_b))

            # This should save the diff but doesn't work ...
            # with open(os.path.join(output, "{}_{}_diff".format(offset_a, offset_b)), "w") as file:
            #    file.write(__store_diff(output, offset_text_dict, offset_a, offset_b))

        break

if __name__ == "__main__":  # This is True if main.py was called from a command line
    main()
