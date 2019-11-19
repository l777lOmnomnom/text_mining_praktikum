# Text_mining
Repository for managing text mining project

# Getting Started

Zugriff auf das Repository:  
Ihr braucht einen SSH key um euren PC zu authentifizieren. Er besteht aus einem geheimen und öffentlichen Teil.   
Gebt nur den Schlüssel in XY.pub raus und nie den anderen. So geht auf Ubuntu:

_____________________________________________________________________________________________________________

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

_____________________________________________________________________________________________________________

Der Teil ab rwby@Rwby:~$ cat .ssh/textmining_rsa.pub  ist der Schlüssel den ich von euch brauche.  


# Git Repo benutzen

- repository auschecken (herunterladen):  
rwby@Rwby:~$ mkdir git  
rwby@Rwby:~$ cd git  
rwby@Rwby:~$ git clone git@github.com:l777lOmnomnom/text_mining.git  

- repository updaten:  
rwby@Rwby:~$ cd git/textmining  
rwby@Rwby:~$ git pull  

- änderungen pushen (hochladen) (vorher git pull!)  
rwby@Rwby:~$ cd git/textmining  
rwby@Rwby:~$ git add file/you/updated.py  
rwby@Rwby:~$ git commit -m "Nachricht mit Beschreibung der Änderung"  
rwby@Rwby:~$ git push  

# Venv benutzen
Virtuelle Umgebungen sind pythons ansatz umgebungsunabhängig Projekte zu verwalten. Anstatt Abhängigkeiten in unseren python-systempfad zu speichern werden sie in der python-umgebung (venv) gespeichert. Somit lassen sich verschiedene Projekte mit widersprüchlichen Abhängigkeiten verwalten. Für uns hat es den Vorteil das ein Package dass wir benutzen wollen sofort allen zur Verfügung steht (und funktioniert).

Geht dafür in eurem Interpreter auf den text-mining ordner des repos, geht in die Einstellungen und zu Projekt Interpreter. Dort wählt ihr (oder fügt neu hinzu) git/textmining/venv/bin/python3 als Interpreter hinzu. Damit habt ihr sofort Zugriff auf simhas/datasketch

Wollt ihr selbst packages installieren und hochladen aktiviert auf der commando-zeile die venv mit   
rwby@Rwby:~$ cd git/textmining  
rwby@Rwby:~$ . venv/bin/activate  
rwby@Rwby:~$ pip install package  
rwby@Rwby:~$ deactivate  
