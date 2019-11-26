import re
import os
import json
import subprocess
# import warcio
# import argparse


class DataHandlerException(Exception):
    """
    This a common convention to have a file specific exception. Usage:

    try:
        your_code()
    except SomeExceptionRaisedByYourCode as err:
        raise DataHandlerException(err)

    It raises the original error but as DataHandlerException to make the failing part more visible
    """
    pass


class __DataHandler:
    def __init__(self, config):
        self.__input = config.get("input")
        self.__output = config.get("output")
        self.__database = config.get("database")

    @property
    def input(self):
        return self.__input

    @input.setter
    def input(self, __i):
        self.__input = __i

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, __o):
        self.__output = __o

    @property
    def database(self):
        return self.__database

    @database.setter
    def database(self, __d):
        self.__database = __d

    def update_database(self, data):
        """

        :param data:
        :return:
        """
        new_data = dict()

        try:
            for dataset in data:
                new_data.update(dataset.dump())

            with open(self.database, "r") as db:
                try:
                    old_data = json.load(db)
                except json.JSONDecodeError:
                    old_data = dict()

            new_data.update(old_data)

            with open(self.database, "w") as db:
                json.dump(new_data, db)
        except Exception as err:
            print("There was a problem updating the database {} with {} \n{}".format(self.database, data, err))
            return False

        return True


class DataHandlerSimHash(__DataHandler):
    def __init__(self, config):
        super(DataHandlerSimHash, self).__init__(config)


class DataHandlerMinHash(__DataHandler):
    def __init__(self, config):
        super(DataHandlerMinHash, self).__init__(config)

        if self.input.split(".")[-1] == "gz":
            print("Input file is an archive. Extracting it to /tmp/output.source")
            self.input = self.__extract_archive(self.input)

    def get_data(self, elements, offset):
        """

        :param elements:
        :param offset:
        :return:
        """
        return_dict, is_finished_flag = self.__read_source(self.input, elements, offset)

        return return_dict, is_finished_flag

    def update_database(self, data):
        """

        :param data:
        :return:
        """
        return super().update_database(data)

    @staticmethod
    def __read_source(input_file, elements, offset=0):
        """
        Reads data from an extracted or compressed warc archive (.source | .warc.gz) and returns a dictonary with
        {source_address1: source_body1, ...}
        If elements if given it will only read so many entries until the given amount is reached.
        If offset if given the returned entries will start with an offset of entries shifted.
        This can be used to iterate through the data without using to much storage.

        :param input_file: path of the extracted source file
        :param elements: the amount of elements you want to retrieve
        :param offset: the offset from the beginning of the file
        :return: result_dict
        """
        line = None  # Placeholder
        is_finished_flag = False
        return_dict = dict()

        with open(input_file, 'r') as source:
            current_elements = 0
            skipped_elements = 0
            source_iterator = iter(source)
            try:
                # Offsets the iterator
                if offset != 0:
                    print(offset)
                    while skipped_elements <= int(offset):
                        line = next(source_iterator)
                        if re.search("<source><location>", line):
                            skipped_elements += 1

                    # Otherwise the header wouldn't be available bellow as the next method continues
                    header = line.split("</location>")[0].replace("<source><location>", "")

                # Create the actual dict with the data extries from offset to elements + offset
                while current_elements < elements:
                    line = next(source_iterator)

                    if re.search("<source><location>", line):
                        header = line.split("</location>")[0].replace("<source><location>", "")
                        current_elements += 1
                        print(current_elements)

                    #  This is stupid but it works
                    elif line is "\n" or id(line) == 140591544343968:
                        continue

                    else:
                        body = return_dict.get(header, "")
                        return_dict.update({header: "{} {}".format(body, line)})
            except StopIteration:
                is_finished_flag = True
                return return_dict, is_finished_flag
            except Exception as err:
                raise DataHandlerException(err)

        return return_dict, is_finished_flag

    # Somehow there is a problem with pathfinding here
    @staticmethod
    def __extract_archive(input_file, output_file="/tmp/output.source"):
        """
        Extracts a warc.gz file. Can also be called from command line via :

        $ python3 datahandler.py -i input_file -o output_file

        :param input_file: Path to the warc.gz archive
        :param output_file: Path to the destination file (default: /tmp/output.source)
        :return:
        """
        current_file_loc = os.path.dirname(os.path.abspath(__file__))

        if not os.path.isfile(input_file):
            raise FileNotFoundError("File {} not found!".format(input_file))

        if os.path.isfile(output_file):
            print("Found existing output file ({}). Renaming it to {}.old and continue ...".format(output_file,
                                                                                                   output_file))
            os.rename(output_file, "{}.old".format(output_file))

        tool_path = os.path.join(current_file_loc, '..', 'tools', 'jwarcex-standalone-2.0.0.jar')
        cmd = "java -jar {} {} {} -c".format(tool_path, input_file, output_file)

        print(cmd)

        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as err:
            print("It looks like there is an issue with path-finding. Copy the link and execute it manually ...")
            print("There was an errror executing the command. Stopping now!")
            print(err)
            exit(1)
        else:
            print("Successfully extracted {} to {}!".format(input_file, output_file))

        return output_file
