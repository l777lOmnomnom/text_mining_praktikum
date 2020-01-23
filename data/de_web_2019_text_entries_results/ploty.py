import json
import collections
import matplotlib.pyplot as plt
import os


input = ["profile_distance_3_simhash", "profile_distance_7_simhash", "profile_distance_10_simhash"]

plt.title("Simhash - time vs elements")
plt.xlabel('elements')
plt.ylabel('time (seconds)')

for file in input:
    with open(file, "r") as _file:
        timings = json.load(_file, object_pairs_hook=collections.OrderedDict)
        hash_time = timings.get("hash")
        find_time = timings.get("find").get("1")

        find_time_per_element = find_time / len(hash_time)


    time = 0
    formatted_timings = collections.OrderedDict()
    for key, value in hash_time.items():
        time = (time + value + find_time_per_element)

        #if divmod(int(key), 5)[1] == 0:
        formatted_timings.update({str(int(key) + 1): time})

    x, y = list(formatted_timings.keys()), list(formatted_timings.values())
    plt.plot(x, y, label="{} {}".format(file.split("_")[1], file.split("_")[2]))
    print(x[-1])
    print(y[-1])

plt.legend(loc="upper left")

plt.savefig("figure_")
