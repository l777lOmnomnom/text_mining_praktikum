import json

with open("de_web_2019_text_entries.json", "r") as file:
    text_dict = json.load(file)

size = int(len(text_dict)/4)
print(size)
i, e = 0, 0
tmp_dict = dict()

for key, value in text_dict.items():
    i += 1
    tmp_dict.update({key: value})

    if i >= size:
        i = 0

        with open("de_web_2019_text_entries_{}.json".format(e),"w") as file:
            e += 1
            json.dump(tmp_dict, file)
        tmp_dict = dict()