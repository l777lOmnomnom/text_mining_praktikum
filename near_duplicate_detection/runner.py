import os
import json

from lib.data_handler import DataHandler, DataHandlerException
from near_duplicate_detection.hasher import Minhash, Simhash, Justushash

implemented_hashes_map = {"simhash": Simhash, "minhash": Minhash, "justushash": Justushash}


class RunnerException(Exception):
    pass


class Runner:
    def __init__(self, name, config):
        self.name = name

        self.diff = None
        self.mode = str()
        self.length = int()
        self.source = str()
        self.dump_text = False
        self.max_length = None
        self.min_length = 0
        self.output_dir = None
        self.max_matches = None
        self.max_elements = int()
        self.matched_offsets = list()
        self.offset_text_map = dict()
        self.offset_hash_map = dict()
        self.additonal_data = dict()

        self.__config = config

        self.init_attributes(config)

        self.data = DataHandler(self.source, self.max_elements)
        self.max_elements = len(self.data.text_dict)
        self.offset_text_map = self.data.text_dict

        self.offset_text_map = self.data.text_dict

        if self.max_length:
            self.length = 0
            self.limit_text_size()

<<<<<<< Updated upstream
        print(len(self.offset_text_map))
=======
>>>>>>> Stashed changes
        self.length = self.data.length

        self.hash_class = implemented_hashes_map.get(self.mode)(self.additonal_data)  # =~ Simhash(self.additional_data)

    def init_attributes(self, config):

        for key, value in config.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                self.additonal_data.update(value)

        if not self.output_dir:
            self.output_dir = "{}_results_small".format(self.source.split(".")[0])

        return

    def create_offset_hash_map(self):
        for offset, text in self.offset_text_map.items():
            self.offset_hash_map.update({offset: self.hash_class.hash(text)})

    def find_similar_hashes(self):
        hashes = self.offset_hash_map.values()
        matches = self.hash_class.find_matches(hashes)

        self.matched_offsets = self.__to_offset_list(matches, self.offset_hash_map)

        print("Found {} matches.".format(len(self.matched_offsets)))

    def dump(self, dump_text=False):
        # Create an output dir in the sources name without all extensionens + _mode (e.g. simhash, minhash, etc)
        print("Creating a results folder in {} and storing all results there.".format(self.output_dir))

        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)

<<<<<<< Updated upstream
        text_size = "{}-{}".format(self.min_length, self.max_length)
        with open(os.path.join(self.output_dir, "profile_{}_{}_{}_elements_{}_size".format(self.name, self.mode, self.max_elements, text_size)), "a") as file:
            json.dump({"config": self.__config,
                       "hash": self.hash_class.hash_time,
                       "find": self.hash_class.find_time,
                       "size": self.length}, file)
=======
        #text_size = "{}-{}".format(self.min_length, self.max_length)
        #with open(os.path.join(self.output_dir, "profile_{}_{}_{}_elements_{}_size".format(self.name, self.mode, self.max_elements, text_size)), "a") as file:
        #    json.dump({"config": self.__config, "hash": self.hash_class.hash_time, "find": self.hash_class.find_time}, file)
>>>>>>> Stashed changes

        for i, match in enumerate(self.matched_offsets):
            if int(match[0] > match[1]):
                offset_a = match[1]
                offset_b = match[0]
            else:
                offset_a = match[0]
                offset_b = match[1]

            with open(os.path.join(self.output_dir, "{}_{}_{}_{}".format(offset_a, offset_b, self.name, self.mode)), "w") as file:
                text_a = self.offset_text_map.get(offset_a)
                text_b = self.offset_text_map.get(offset_b)
                try:
                    self.diff = self.__diff(text_a, text_b)
                except Exception:
                    self.diff = "None found. Error"

                infos = "Config:\n{}\nTextlength: {}\nDifflength: {}\nSim: {}".format(self.__config,
                                                                             int(0.5 * len(text_a) + len(text_b)),
                                                                             len(self.diff[0] + self.diff[1]),
                                                                                      match[2])

                text_a = "Offset: {}\nHash: {}\nMisses:\n{}\n".format(offset_a,
                                                                      self.offset_hash_map.get(offset_a),
                                                                      self.diff[0])

                text_b = "Offset: {}\nHash: {}\nMisses:\n{}\n".format(offset_b,
                                                                      self.offset_hash_map.get(offset_b),
                                                                      self.diff[1])
                if dump_text:
                    text_a = text_a + "Text:\n{}".format(text_a)
                    text_b = text_b + "Text:\n{}".format(text_b)

                file.write("{}\n\n{}\n\n{}\n\n{}".format(infos, text_a, "#"*25, text_b))

            if self.max_matches:
                i += 1
                if i >= self.max_matches:
                    print("Stopping after {} matches have been dumped. Text dumping is {}.".format(self.max_matches,
                                                                                                   self.dump_text))
                    break

            #x.append(int(0.5 * (len(text_a) + len(text_b))))
            #y.append(len(self.diff[0]) + len(self.diff[1]))
        #self.__plot(self.name, x, y)
        

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
                    offset_list.append((offset_a, offset_b, hash_tuple[2]))
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

    def limit_text_size(self):
        print("Limiting text size to {} ...".format(self.max_length))
        tmp_dict = dict()
        for offset, text in self.offset_text_map.items():
            if len(text) <= self.max_length and len(text) >= self.min_length:
                tmp_dict.update({offset: text})
                self.length += len(text)

        print("Now {} elements are loaded".format(len(tmp_dict)))
        self.offset_text_map = tmp_dict
