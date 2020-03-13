import os
import json

from lib.config_handler import Config
from lib.data_handler import Data
from lib.hash_handler import Hash


class RunnerException(Exception):
    pass


class Runner:
    def __init__(self, name, config):
        self.__name = name

        # Create a config class
        self.__config = Config(config)

        # Create an iterable Data class which yields offset, text from the archive
        self.data = Data(self.config.source)
        self.data_iterator = self.data

        # Create the Hash class
        self.hasher = Hash(self.config.hash_data)

        # Maps to keep track of offset - hash - text
        self.__offset_text_map = dict()
        self.__offset_hash_map = dict()

        self.__matched_offsets = list()

    @property
    def name(self):
        return self.__name

    @property
    def config(self):
        return self.__config

    def hash(self):
        """
        Start the hashing process with the configured hashing algorithm. The hasher tracks its time by itself.

        :return:
        """
        for offset, text in next(self.data_iterator):
            hash = self.hasher.hash(text)
            self.__offset_text_map.update({offset: text})
            self.__offset_hash_map.update({offset: hash})

        return

    def find_similar_hashes(self):
        """
        Finds similar matches and creates a list for all matched hashes where a offset tuple belonging to the match
        can be found.

        :return:
        """
        matches = self.hasher.find_matches(self.__offset_hash_map.values())

        print("Formatting the found matches. This takes some time ...")
        self.__matched_offsets = self.__to_offset_list(matches, self.__offset_hash_map)

        print("Found {} matches.".format(len(self.__matched_offsets)))

        return

    def dump(self):
        """
        Dumps all results accoring to the settings in the config.

        :return:
        """
        print("Creating a results folder in {} and storing all results there.".format(self.config.output_dir))

        if not os.path.isdir(self.config.output_dir):
            os.mkdir(self.config.output_dir)

        profile_file_name = "{}_{}_profile".format(self.name, self.config.mode)

        print("Dumping profile ...")
        with open(os.path.join(self.config.output_dir, profile_file_name), "a") as file:
            profile = {"config": self.config, "hash": self.hasher.hash_time_dict, "find": self.hasher.find_time_dict}
            json.dump(profile, file)

        print("Dumping matches ...")
        for i, match in enumerate(self.__matched_offsets):
            if int(match[0] > match[1]):
                offset_a = match[1]
                offset_b = match[0]
            else:
                offset_a = match[0]
                offset_b = match[1]

            match_file_name = "{}_{}_{}_{}".format(self.name, self.config.mode, offset_a, offset_b)
            with open(os.path.join(self.config.output_dir, match_file_name), "w") as file:
                infos = "Config:\n: {}".format(self.config)

                if self.config.dump_text:
                    text_a = "Text:\n{}".format(self.__offset_text_map.get(offset_a))
                    text_b = "Text:\n{}".format(self.__offset_text_map.get(offset_b))

                file.write("{}\n\n{}\n\n{}\n\n{}".format(infos, text_a, "#"*25, text_b))


            #x.append(int(0.5 * (len(text_a) + len(text_b))))
            #y.append(len(self.diff[0]) + len(self.diff[1]))
            #self.__plot(self.name, x, y)"""

        return

    @staticmethod
    def __to_offset_list(matches, offset_hash_map):
        """
        Converts a list of matched hashes to a dict where the offsets in the warc archive off the different hashes is key
        and the hash is the valie. Necessary helper function.

        :param matches:
        :param offset_hash_map:
        :return:
        """

        offset_list = list()

        for hash_tuple in matches:
            offset_a, offset_b = None, None
            for offset, hash in offset_hash_map.items():
                if hash == hash_tuple[0]:
                    offset_a = offset
                elif hash == hash_tuple[1]:
                    offset_b = offset

                # Stops if both have been found
                if offset_a and offset_b:
                    offset_list.append((offset_a, offset_b))
                    break

        return offset_list

    @staticmethod
    def __diff(text_a, text_b):
        """
        Doesn't work :/

        :param output_path:
        :param _offset_text_dict:
        :param offset_a:
        :param offset_b:
        :return:
        """
        import difflib

        diff = None

        try:
            diff = [li for li in difflib.ndiff(text_a, text_b) if li[0] != ' ']
        except TypeError as err:
            print(err)

        diff_a = ""
        diff_b = ""

        if not diff:
            return ("There was a problem with the diff!", "There was a problem with the diff!")

        for _diff in diff:
            if "+" in _diff:
                diff_a += _diff.replace("+ ", "")
            elif "-" in _diff:
                diff_b += _diff.replace("- ", "")

        return (diff_a, diff_b)

    @staticmethod
    def __plot(name, x, y):
        import matplotlib.pyplot as plt

        plt.plot(x, y)
        plt.xlabel('text length')
        plt.ylabel('diff length')
        plt.savefig("figure_{}".format(name))
