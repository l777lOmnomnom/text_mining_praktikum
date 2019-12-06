# Text_mining
Repository for managing text mining project

# Getting Started

Zugriff auf das Repository:  
Ihr braucht einen SSH key um euren PC zu authentifizieren. Er besteht aus einem geheimen und öffentlichen Teil.   
Gebt nur den Schlüssel in XY.pub raus und nie den anderen. So geht auf Ubuntu:

_____________________________________________________________________________________________________________
```
rwby@Rwby:~$ ssh-keygen -t rsa -b 4096 -C "robby.wagner1991@web.de"  
Generating public/private rsa key pair.  
Enter file in which to save the key (/home/rwby/.ssh/id_rsa): /home/rwby/.ssh/textmining_rsa  
Enter passphrase (empty for no passphrase):   
Enter same passphrase again:   
Your identification has been saved in /home/rwby/.ssh/textmining_rsa.  
Your public key has been saved in /home/rwby/.ssh/textmining_rsa.pub.  
The key fingerprint is:  
  
...  
rwby@Rwby:~$ ll .ssh/  
total 28  
drwx------  2 rwby rwby 4096 Nov 16 15:18 ./  
drwxr-xr-x 24 rwby rwby 4096 Nov 16 15:12 ../  
-rw-------  1 rwby rwby 3326 Nov 12 13:26 id_rsa  
-rw-r--r--  1 rwby rwby  749 Nov 12 13:26 id_rsa.pub  
-rw-r--r--  1 rwby rwby  884 Nov 12 15:20 known_hosts
-rw-------  1 rwby rwby 3326 Nov 16 15:18 textmining_rsa        <- PRIVATER SCHLÜSSEL  
-rw-r--r--  1 rwby rwby  749 Nov 16 15:18 textmining_rsa.pub    <- ÖFFENTLICHER SCHLÜSSEL  
rwby@Rwby:~$ cat .ssh/textmining_rsa.pub   
ssh-rsa ...== robby.wagner1991@web.de
```
_____________________________________________________________________________________________________________

Der Teil ab rwby@Rwby:~$ cat .ssh/textmining_rsa.pub  ist der Schlüssel den ich von euch brauche.  


# Git Repo benutzen

- repository auschecken (herunterladen):  
```
rwby@Rwby:~$ mkdir git  
rwby@Rwby:~$ cd git  
rwby@Rwby:~$ git clone git@github.com:l777lOmnomnom/text_mining.git  
```
- repository updaten:  
```
rwby@Rwby:~$ cd git/textmining  
rwby@Rwby:~$ git pull  
```
- änderungen pushen (hochladen) (vorher git pull!)  
```
rwby@Rwby:~$ cd git/textmining  
rwby@Rwby:~$ git add file/you/updated.py  
rwby@Rwby:~$ git commit -m "Nachricht mit Beschreibung der Änderung"  
rwby@Rwby:~$ git push  
```

# Venv benutzen
Virtuelle Umgebungen sind pythons ansatz umgebungsunabhängig Projekte zu verwalten. Anstatt Abhängigkeiten in unseren python-systempfad zu speichern werden sie in der python-umgebung (venv) gespeichert. Somit lassen sich verschiedene Projekte mit widersprüchlichen Abhängigkeiten verwalten. Für uns hat es den Vorteil das ein Package dass wir benutzen wollen sofort allen zur Verfügung steht (und funktioniert).

Geht dafür in eurem Interpreter auf den text-mining ordner des repos, geht in die Einstellungen und zu Projekt Interpreter. Dort wählt ihr (oder fügt neu hinzu) git/textmining/venv/bin/python3 als Interpreter hinzu. Damit habt ihr sofort Zugriff auf simhas/datasketch

Wollt ihr selbst packages installieren und hochladen aktiviert auf der commando-zeile die venv mit   
```
rwby@Rwby:~$ cd git/textmining  
rwby@Rwby:~$ . venv/bin/activate  
rwby@Rwby:~$ pip install package  
rwby@Rwby:~$ deactivate  
```

# Python Project Struktur
Derzeit besteht die Implementation aus 4 Teilen:
- conf/example.conf
  Die Beispielconfig, sie enthält parameter die zum Ausführen des Programmes benötigt werden im {key: value} Format.
  Bsp:
```JSON  
  {
    "mode": "update_hash_db",
    "elements": 1000,
    "archive": "/home/omnomnom/git/text_mining/examples/de_web_2019.01000.warc.gz",
    "shingle_size": 3
  }
```
- main.py | main.py -c path/to/config.conf
  Lädt die Standardconfig (conf/example.conf) oder eine config die durch -c angegeben werden kann.
  Nachdem die Config geladen wurde überprüft das script ob die config einen Key "mode" enthält.
  Existiert dieser wird im letzten Teil des scriptes anhand einer if schleife entschieden was getan werden soll
```python
    if not config.get('mode'):
        raise NotImplemented("No mode specified. This is not implemented!")

    elif config.get('mode') == "update_hash_db":
        sim_hash.Simhash(config).update_hash_db()
        min_hash.Minhash(config).update_hash_db()

    elif config.get("mode") == "update_min_hash_jaccard_matrix":
        pass

    elif config.get("mode") == "simhash":
        sim_hash.Simhash(config)  
```
- near_document_detection/xy_hash.py
  Diese scripte werden über main.py angesteuert und mit der config initiert. Hier kommt die eigentliche Logik der 
  Impelmentierung hin. Wollt ihr einen Parameter aus der config an eure Klasse übergeben fügt diesen eurer Config
  als {"config_eintrag": "wert"} hinzu.
  In eurer Klasse könnt ihr dann mit config.get("config_eintrag", "default wert wenn nicht in config") darauf zugreifen
  (und einen default wert festlegen)
  Bsp:
```python  
  class Minhash:
    def __init__(self, config):
        self.data_handler = data_handler.DataHandlerMinHash()

        self.__input = config.get("archive")
        self.__database = config.get("database")
        self.__elements = config.get("elements", 1000)
        self.__offset = config.get("offset", 0)
        self.__all = config.get("all", False)
        
  ...
        
  def estimate_jaccard_sim(self, data):
    """ This estimates the jaccard similarity between all entries in a set of min hashes. The results are stored
        in a special database.

    :return:
    """
    est_dict = dict()
    i = 0
    for offset1, hash1 in data.items():
        i += 1
        j = 0
        for offset2, hash2 in data.items():
            j += 1
            if j > i:
                est_dict.update({"{}#{}".format(offset1, offset2): self.__estimate_jaccard_sim(hash1, hash2)})

    return

@staticmethod
def __estimate_jaccard_sim(minhash1, minhash2):
    """

    :param body_tuple:
    :return:
    """
    return minhash1.jaccard(minhash2)
```

- lib/data_handler.py
  Der DataHandler besteht aus einer Basis Klasse (_DataHandler) der die grundlegende Arbeit mit den Daten übernimmt. 
  Bisher kann er aus einem Archiv eine Datenbank mit Hashes der jeweiligen Einträge erzeugen und diese Datenbank
  speichern.
  Welche Hash Fuktion hierbei benutzt wird hängt von der Elternklasse ab die jeweils ihre eigenen Fuktionen
  Implementieren. Bisher existiert eine DataHandlerSimHash und DataHandlerMinHash.
  Ihn euren near_duplicate_detection/xy_hash.py scripten solltet ihr niemand die Basis Klasse benutzen.
  Erzeugt eine neue Elternklasse und erbt von _DataHandler. Ein Beispiel für SimHash:
```python  
class __DataHandler:
    def __init__(self):
        self.mode = None
    
    ...
    
    def get_hash_list(self, input_file, elements=1000, offset=0):
        """
        This calculates the hashes for a given archive. The parent class gives the used hash function.

        :param input_file: the input archive
        :param elements: the amount of elements retrieved at once
        :param offset: the offset which determines from which starting element and amount of elements is retrieved

        :return: hash data base as {offset: {"min_hash": {minhash, "sim_hash": simhash}}
        """
       
        with open("/home/omnomnom/git/text_mining/data/archives/de_web_2019.01000.warc.gz", 'rb') as stream:
            archive_stream = ArchiveIterator(stream)
            for record in archive_stream:
                ...
                    else:
                        i += 1
                        # The parent class should implement this hash function.
                        _hash = self.hash(text)

                        ...
        return hash_db

    def hash(self, text):
        """
        The base class will not implement a hash function because the hash function derives from the parent class

        :param text:
        :return:
        """
        raise ModuleNotFoundError("Dont call the base class ...")
```
  Wie du siehst wirft die Funktion hash(text) eine ModuleNotFound Exception. Das liegt daran dass genau diese Funktion
  von der Elternklasse zur Verfügung gestellt werden soll:
```python  
class DataHandlerSimHash(__DataHandler):
    def __init__(self, shingle_size):
        super(DataHandlerSimHash, self).__init__()
        self.mode = "simhash"
        self.shingle_size = shingle_size

    def get_hash_list(self, input_file, elements=1000, offset=0):
        return super().get_hash_list(input_file, elements, offset)

    def hash(self, text):
        shingles = (' '.join(tokens) for tokens in simhash.shingle(self.tokenize(text), self.shingle_size))

        return simhash.compute([ctypes.c_ulong(hash(shingle)).value for shingle in shingles])

    @staticmethod
    def tokenize(text):
        tokens = re.split("\s+", re.sub(r'[^\w\s]', '', text.lower()))
        # print(tokens)
        return tokens
```  
