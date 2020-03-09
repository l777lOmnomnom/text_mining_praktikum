import pandas as pd
from warcio import ArchiveIterator
import simhash
import re
import ctypes
import json
import time
from bs4 import BeautifulSoup

utf_8 = ['text/html; charset=UTF-8',
         'text/html; charset=utf-8',
         'text/html;charset=UTF-8',
         'text/html;charset=utf-8',
         'text/html; Charset=UTF-8',
         'text/html; Charset=utf-8;charset=UTF-8',
         'text/html; charset=utf8']

informations = []
hashes = []

def tokenize(text):
    tokens = re.split("\s+", re.sub(r'[^\w\s]', '', text.lower()))
    #print(tokens)
    return tokens

def shingle(text):
    shingles = list(simhash.shingle(tokenize(text), 3))
    print(shingles)
    return shingles

def extract(record, parser, encoding):
    soup = BeautifulSoup(record.content_stream, parser, from_encoding=encoding)
    return soup.body.get_text(separator=' ')

def makeSimhash(text):
    shingles = (' '.join(tokens) for tokens in simhash.shingle(tokenize(text), 3))

    return simhash.compute([ctypes.c_ulong(hash(shingle)).value for shingle in shingles])


start_time = time.time()
with open('/home/alex/Downloads/de_web_2019.01000.warc.gz', 'rb') as stream:
    i = 0
    archiveStream = ArchiveIterator(stream)
    for record in archiveStream:
        if record.rec_type == 'response' and record.http_headers.get_header('Content-Type') in utf_8:
            soup = BeautifulSoup(record.content_stream(), 'lxml', from_encoding='utf-8')
            for script in soup(["script", "style"]):
                script.extract()


            try:
                text = soup.body.get_text(separator=' ')
                lines = (line.strip() for line in text.splitlines())
                # break multi-headlines into a line each
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # drop blank lines
                text = '\n'.join(chunk for chunk in chunks if chunk)

            except AttributeError as err:
                print('Wrong Encoding at offset ' + str(archiveStream.get_record_offset()))


            #print(text)
            #print(shingle(text))
            #print(makeSimhash(text))
            #print(format(makeSimhash(text), '064b'))
                #print(archiveStream.get_record_offset())
            else:
                sim_hash = makeSimhash(text)
                data_dict = {"Record-No:": i,
                             "Record-Offset": archiveStream.get_record_offset(),
                             "Hash-Value": sim_hash,
                             "64bit": format(sim_hash, '064b'),
                             "Similar Documents": []}
                informations.append(data_dict)

                hashes.append(sim_hash)
                print(i)
                i = i + 1
        if archiveStream.get_record_offset() == 12904907 or archiveStream.get_record_offset() == 4633925:
            print(shingle(text))

        if i > 1000:
            archiveStream.close()
            break

    print("--- %s seconds --- End of Hashing" % (time.time() - start_time))

    matches = simhash.find_all(hashes, 8, 6)






print("--- %s seconds --- End of finding similar hashes" % (time.time() - start_time))

with open ('/tmp/data.json', 'w') as file:
    json.dump(informations, file)
print("--- %s seconds --- End of Writing JSON file" % (time.time() - start_time))
with open('/tmp/similiar_data.txt', 'w') as file:
        file.write('\n'.join('%s %s' % x for x in matches))


print("--- %s seconds ---" % (time.time() - start_time))