import os
import sys
import json


class ConfigException(Exception):
    pass


class Config:
    def __init__(self, config):
        self.__config = str()
        self.__mode = str()
        self.__source = str()
        self.__dump_text = False
        self.__output_dir = str()
        self.__hash_data = dict()

        self.config = config

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, config):
        if os.path.isfile(str(config)):
            self.__config = config
        else:
            raise ConfigException("{} is not a file!".format(config))

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, __mode):
        self.__mode = __mode

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, __source):
        self.__source = __source

    @property
    def dump_text(self):
        return self.__dump_text

    @dump_text.setter
    def dump_text(self, __dump_text):
        self.__dump_text = __dump_text

    @property
    def output_dir(self):
        return self.__output_dir

    @output_dir.setter
    def output_dir(self, __output_dir):
        self.__output_dir = __output_dir

    @property
    def hash_data(self):
        return self.__hash_data

    @hash_data.setter
    def hash_data(self, __hash_data):
        self.__hash_data = __hash_data

    @property
    def bool_map(self):
        return {"True": True, "False": False}

    def load(self):
        """ This is the first function to be called. It will load all config entries from the config file.
        You can specify a config by calling this script with -c /path/to/conf.file
        All values loaded from the config are stored in a dictionary and handed to the runner.

        :return:
        """
        try:
            with open(self.config, "r") as conf:
                conf = json.load(conf)
        except IOError as err:
            print("Failed to load config: {}".format(err))
            sys.exit(1)
            
        print("#########################   CONFIG   #########################\n")

        for key, value in conf.items():
            print("    {}:".format(key))
            if hasattr(self, key):
                setattr(self, key, value)

            if key == "hash_data":
                for _key, _value in value.items():
                    print("        {}: {}".format(_key, _value))

        print("\n############################################################\n")