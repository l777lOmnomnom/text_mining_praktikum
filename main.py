import sys
import argparse
import cProfile
import pstats
import json
import os

# This is command line parser, its quite self explanatory
parser = argparse.ArgumentParser()  # This is the cmd-line parser
parser.add_argument("-c", "--config", help="path to the config file")

args = parser.parse_args()


if __name__ == "__main__":  # This is True if main.py was called from a command line
    """
    You can specify a config by calling this script with -c /path/to/conf.file
    """
    from near_duplicate_detection.runner import Runner

    if not os.path.isfile(args.config):
        raise SystemExit("Parameter -c missing!")
    else:
        with open(args.config, "r") as file:
            runner_config = json.load(file)

    for run_name, run_config in runner_config.items():
        # Threading could be added here
        runner = Runner(run_name, run_config)

        print("\nHashing ...")
        __hash = runner.create_offset_hash_map()

        print("Searching ...")
        __find = runner.find_similar_hashes()

        print("Dumping ...")
        runner.dump()

        #cProfile.run("__hash()", "{}/profile_calculate_hashes_{}_{}".format(runner.output_dir, run, runner.length))
        #cProfile.run("__find()", "{}/profile_find_similar_hashes_{}_{}".format(runner.output_dir, run, runner.length))

        #p1 = pstats.Stats("{}/profile_calculate_hashes_{}_{}".format(runner.output_dir, run, runner.length))
        #p2 = pstats.Stats("{}/profile_find_similar_hashes_{}_{}".format(runner.output_dir, run, runner.length))

        #p1.strip_dirs().sort_stats(-1).dump_stats("{}/times_calculate_hashes_{}_{}".format(runner.output_dir, run, runner.length))
        #p2.strip_dirs().sort_stats(-1).dump_stats("{}/times_find_similar_hashes_{}_{}".format(runner.output_dir, run, runner.length))
