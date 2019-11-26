import re
import os
import json
import subprocess
import warcio
import argparse

FILE = os.path.dirname(os.path.abspath(__file__))

# BESXHREIBÄHDKFH
def get_header_body_dict(file, elements=1000, offset=0):
    """ ### Should be especially used for test purpose ###
    Returns a dictonary containing elements amount of entries with {html_header_info: html_text}.
    The offset and elements can be used to iterate through a large file step by step instead of loading it all.
    :param file:
    :param elements:
    :param offset:
    :return:
    """
    return __read_source(file, elements, offset)


def update_database_jaccard(datasets, database=os.path.join(FILE, "data/db")):
    """

    :param data:
    :return:
    """
    new_data = dict()
    for dataset in datasets:
        new_data.update(dataset.dump())

    with open(database, "r") as db:
        try:
            old_data = json.load(db)
        except Exception:
            old_data = dict()

    new_data.update(old_data)

    with open(database, "w") as db:
        json.dump(new_data, db)


def __read_source(input_file, elements=500, offset=0):
    """
    Reads data from an extracted warc.gz and yields a dict with {str(header): str(body)}
    There is a default max element size of 1000 and an offset if you want to get elements somewhere in the data set.

    :param input_file: path of the extracted source file
    :param elements: the amount of elements you want to retrieve
    :param offset:
    :return: result_dict
    """
    line = None  # Placeholder
    return_dict = dict()

    if input_file.split(".")[-1] is "gz":
        print("Input file is an archive. Extracting it now ...")
        input_file = __extract_archive(input_file)

    with open(input_file, 'r') as source:

        current_elements = 0
        skipped_elements = 0
        source_iterator = iter(source)

        # Offsets the iterator
        if offset != 0:
            print(offset)
            while skipped_elements <= int(offset):
                line = next(source_iterator)
                if re.search("<source><location>", line):
                    skipped_elements += 1

            header = line  # Otherwise the header wouldn't be available bellow as the next method continues

        # Create the actual dict with the data extries from offset to elements + offset
        while current_elements < elements:
            line = next(source_iterator)

            if re.search("<source><location>", line):
                header = line
                current_elements += 1

            #  This is stupid but it works
            elif line is "\n" or id(line) == 140591544343968:
                continue

            else:
                # If you want to add your own return format add the return objects definition in the beginning of the
                # function and fill it here with the payload here (or with header infos above) (return x, y, z).
                body = return_dict.get(header, "")
                return_dict.update({header: "{} {}".format(body, line)})

    return return_dict


# Somehow there is a problem with pathfinding here
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
        print("Found existing output file ({}). Renaming it to {}.old and continue ...".format(output_file, output_file))
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
