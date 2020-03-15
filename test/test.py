import os
import json
import subprocess

config_dict = {"mode": "simhash", "source": "test.warc.gz", "dump_text": "False", "output_dir": "test_results",
               "hash_data": {"shingle_size": 12, "distance": 4, "blocks": 10, "store_duplicates": "False"}}

with open("/tmp/tmp.config", "w") as config:
    json.dump(config_dict, config)

current_path = os.path.dirname(os.path.abspath(__file__))
print([". {}/../venv/bin/activate".format(current_path), "&&", "python3 ../main.py -c /tmp/tmp.config"])
subprocess.call([". {}/../venv/bin/activate".format(current_path), "&&", "python3 ../main.py -c /tmp/tmp.config"],
                      shell=True)
