import argparse
import json
import os

parser = argparse.ArgumentParser()  # This is the cmd-line parser
parser.add_argument("-c", "--config", help="path to the config file")

args = parser.parse_args()


if __name__ == "__main__":  # This is True if main.py was called from a command line
    """
    You can specify a config by calling this script with -c /path/to/conf.file
    """
    from near_duplicate_detection.runner import Runner

    if not args.config:
        raise SystemExit("Parameter -c missing!")

    if not os.path.isfile(args.config):
        raise SystemExit("Config not found: {}".format(args.config))
    else:
        with open(args.config, "r") as file:
            runner_config = json.load(file)

    for run_name, run_config in runner_config.items():
        # Threading could be added here
        runner = Runner(run_name, run_config)

        print("\nHashing ...\n")
        __hash = runner.hash()

        print("\nSearching ...")
        __find = runner.find_similar_hashes()

        print("\nDumping ...")
        runner.dump()
