import re
import os
import subprocess
import warcio
import argparse


def get_data(input_file, elements=500):
    """
    Reads data from an extracted warc.gz and yields a list with the different elements.
    There is a default max element size of 1000 and an offset if you want to get elements somewhere in the data set.

    :param input_file: path of the extracted source file
    :param elements: the amount of elements you want to retrieve
    :param offset: NotImplemented()
    :return: result_dict
    """
    return_dict = dict()

    with open(input_file, 'r') as source:

        current_elements = 0
        source_iterator = iter(source)

        while current_elements < elements:
            line = next(source_iterator)

            if re.search("<source><location>", line):
                header = line
                current_elements += 1

            #  This is stupid but it works
            elif line is "\n" or id(line) == 140591544343968:
                continue

            else:
                body = return_dict.get(header, "")
                return_dict.update({header: "{} {}".format(body, line)})

    return return_dict


# Somehow there is a problem with pathfinding here
def extract_archive(input_file, output_file="/tmp/output.source"):
    """
    Extracts a warc.gz file. Can also be called from command line via :

    $ python3 datahandler.py -i input_file -o output_file

    :param input_file: Path to the warc.gz archive
    :param output_file: Path to the destination file (default: /tmp/output.source)
    :return:
    """
    size = None  # Not implemented
    current_file_loc = os.path.dirname(os.path.abspath(__file__))

    if not os.path.isfile(input_file):
        raise FileNotFoundError("File {} not found!".format(input_file))

    if os.path.isfile(output_file):
        print("Found existing output file ({}). Renaming it to {}.old and continue ...")
        os.rename(output_file, "{}.old".format(output_file))

    tool_path = os.path.join(current_file_loc, 'tools', 'jwarcex-standalone-2.0.0.jar')
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

    return


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="path of an archive")
parser.add_argument("-o", "--output", help="path of the destination")
args = parser.parse_args()

if __name__ == "__main__":
    extract_archive(args.input, args.output)
