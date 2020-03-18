import os
import sys
import json


class ConfigException(Exception):
    pass


class Config:
    """
    This is the config class. It has class attributes for all parameter the config supports. If you need more config
    parameter just add a setter and getter for it in here.
    """
    def __init__(self, config):
        self.__config = str()
        self.__mode = str()
        self.__source = str()
        self.__dump_graph = False
        self.__dump_text = False
        self.__max_elements = 0
        self.__output_dir = str()
        self.__hash_data = dict()

        self.load(config)  # Loads the config

    @property
    def config(self):
        """
        Returns path to config file

        :return: str() - config path
        """
        return self.__config

    @config.setter
    def config(self, config):
        """
        Setter for config path

        :param config: str() - config path
        """
        if os.path.isfile(str(config)):
            self.__config = config
        else:
            raise ConfigException("{} is not a file!".format(config))

    @property
    def mode(self):
        """
        Returns the chosen hashing mode

        :return: str() - hashing mode
        """
        return self.__mode

    @mode.setter
    def mode(self, mode):
        """
        Setter for hashing mode

        :param mode: str() - hashing mode
        """
        self.__mode = mode

    @property
    def source(self):
        """
        Path to warc IO archive

        :return: str() - path to warc IO archive
        """
        return self.__source

    @source.setter
    def source(self, __source):
        """
        Setter for the warc IO archives source

        :param __source:
        :return:
        """
        self.__source = __source

    @property
    def dump_text(self):
        """
        Returns dump_text flag (True or False)

        :return: bool() - dump_text_flag
        """
        return self.__dump_text

    @dump_text.setter
    def dump_text(self, dump_text):
        """
        Setter for dump_text flag

        :param dump_text: bool() - dump_text_flag
        """
        self.__dump_text = dump_text

    @property
    def dump_graph(self):
        """
        Returns dump_graph flag (True or False)

        :return: bool() - dump_graph_flag
        """
        return self.__dump_graph

    @dump_graph.setter
    def dump_graph(self, dump_graph):
        """
        Setter for dump_text flag

        :param dump_graph: bool() - dump_graph_flag
        """
        self.__dump_graph = dump_graph

    @property
    def max_elements(self):
        """
        Returns the maximum elements to be hashed from the archive

        :return: int() - maximum elements to hash
        """
        return self.__max_elements

    @max_elements.setter
    def max_elements(self, max):
        """
        Setter for hashing mode

        :param max: int() - maximum elements
        """
        self.__max_elements = max

    @property
    def output_dir(self):
        """
        Returns path to directory where the results are stored

        :return: str() - output_dir
        """
        return self.__output_dir

    @output_dir.setter
    def output_dir(self, output_dir):
        """
        Setter for the path of the output dir

        :param output_dir: str() - output_dir
        """
        self.__output_dir = output_dir

    @property
    def hash_data(self):
        """
        Returns the hash data as dict which is supplied to the hashing class.

        :return: dict() - hash_data
        """
        return self.__hash_data

    @hash_data.setter
    def hash_data(self, hash_data):
        """
        Setter for the hashing data

        :param hash_data: dict() - hash_data
        """
        self.__hash_data = hash_data

    @property
    def bool_map(self):
        """
        Translate a True or False string to boolean.

        :return: bool()
        """
        return {"True": True, "False": False}

    def load(self, config):
        """
        This function is called on class-creation. It will load all config entries from the config file.
        All values loaded from the config are stored as class arguments.

        :param config: config dict.
        :return:
        """
        print("#########################   CONFIG   #########################\n")

        for key, value in config.items():

            if hasattr(self, key):
                if key == "hash_data":
                    for _key, _value in value.items():
                        print("        {}: {}".format(_key, _value))
                else:
                    setattr(self, key, value)
                    print("    {}: {}".format(key, value))

        print("\n##############################################################")

        return self

    def dump(self):
        """
        This functions dumps the config into a dict.

        :return: dict() - config as a dict.
        """
        ret = {"mode": self.mode, "source": self.source, "dump_text": self.dump_text, "output_dir": self.output_dir,
               "hash_data": self.hash_data}

        return ret
