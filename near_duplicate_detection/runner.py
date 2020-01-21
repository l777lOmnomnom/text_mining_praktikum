import os

from lib.data_handler import DataHandler, DataHandlerException
from near_duplicate_detection.hasher import Minhash, Simhash, Justushash

implemented_hashes_map = {"simhash": Simhash, "minhash": Minhash, "justushash": Justushash}


class RunnerException(Exception):
    pass


class Runner:
    def __init__(self, name, config):
        self.name = name

        self.mode = str()
        self.source = str()
        self.output_dir = str()
        self.max_elements = int()
        self.matched_offsets = list()
        self.offset_text_map = dict()
        self.offset_hash_map = dict()
        self.additonal_data = dict()

        self.__config = config

        self.init_attributes(config)

        self.data = DataHandler(self.source, self.max_elements)
        self.hash_class = implemented_hashes_map.get(self.mode)(self.additonal_data) # =~ Simhash(self.additional_data)

    def init_attributes(self, config):
        for key, value in config.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                self.additonal_data.update({key, value})

        return

    def create_offset_hash_map(self):
        for offset, text in self.offset_text_map.items():
            self.offset_hash_map.update({offset: self.hash_class.hash(text)})

    def find_similar_hashes(self):
        hashes = self.offset_hash_map.values()
        matches = self.hash_class.find_matches(hashes)

        self.matched_offsets = self.__to_offset_list(matches, self.offset_hash_map)

    def dump(self):
        for match in self.matched_offsets:

            if int(match[0] > match[1]):
                offset_a = match[1]
                offset_b = match[2]
            else:
                offset_a = match[0]
                offset_b = match[1]

            # Create an output file in the output_dir + _offset_a_offset_b_run
            with open(os.path.join(self.output_dir, "{}_{}_{}_{}".format(offset_a, offset_b, self.name, self.mode)), "w") as file:
                infos = "Config:\n{}".format(self.__config)
                text_a = "Offset: {}\nHash: {}\nLength: {}\n\n{}".format(offset_a,
                                                                         self.offset_hash_map.get(offset_a),
                                                                         len(self.offset_text_map.get(offset_a)),
                                                                         self.offset_text_map.get(offset_a))

                text_b = "Offset: {}\nHash: {}\nLength: {}\n\n{}".format(offset_b,
                                                                         self.offset_hash_map.get(offset_b),
                                                                         len(self.offset_text_map.get(offset_b)),  # noqa
                                                                         self.offset_text_map.get(offset_b))  # noqa

                file.write("{}\n\n{}\n\n{}\n\n{}".format(infos, text_a, "#"*25, text_b))

            # This should save the diff but doesn't work ...
            # with open(os.path.join(output, "{}_{}_diff".format(offset_a, offset_b)), "w") as file:
            #    file.write(__store_diff(output, offset_text_dict, offset_a, offset_b))


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
        offset_a, offset_b = None, None
        for hash_tuple in matches:
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

        # Create an output dir in the sources name without all extensionens + _mode (e.g. simhash, minhash, etc)
        output_dir = "{}".format(source.split(".")[0])
        print("Creating a results folder in {} and storing all results there.".format(output_dir))
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)