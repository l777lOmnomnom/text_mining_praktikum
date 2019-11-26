warc = open("de_web_2019.01016_2.txt", "r") #replace with own doc
newFile = open("hashes" + ".txt", "w+")


def split(word):
    return [char for char in word]


text = ""
cut = ""
prevLoc = ""
prevSim = "1"*64
loc = ""
shingles = []
h = 0
d = 0
similarity = []

def getSim(shingles):
    print("hashing...")
    sim = "0"*64
    sim = split(sim)
    
    for sh in shingles:
        #print(sh)
        h = bin(hash(sh))
        #print(h)
        
        if h.startswith("0"):
            #print("-------------------------------------------")
            h = h[2:len(h)]
            if len(h) < 64:
                h = (64-len(h))*'0' + h
            #print(h)
            
        if h.startswith("-"):
            #print("-------------------------------------------")
            h = h[3:len(h)]
            if len(h) < 64:
                h = (64-len(h))*'0' + h
            #print(h)
        
        h = str(h)
        
        #sim = split(sim)
        
        #print("sim:")
        #print(sim)
        
        for i in range(0, len(h)):
            #print("i " + str(i))
            if h[i] == "1":
                #print("simadd")
                #print(sim[i])
                sim.insert(i, str(int(sim[i]) + 1))
                sim.pop(i+1)
                #sim = sim[i-abs(i-1):i+1] + str(int(sim[i]) + 1) + sim[i+1:]
                
            
            if h[i] == "0":
                #print("simdiv")
                #print(sim[i])
                sim.insert(i, str(int(sim[i]) - 1))
                sim.pop(i+1)
                #sim = sim[i-abs(i-1):i+1] + str(int(sim[i]) - 1) + sim[i+1:]
                
            
            #print(sim)
            
    
    for i in range(0, len(sim)):
        if int(sim[i]) <= 0:
            sim.insert(i, "0")
            sim.pop(i+1)
            
        if int(sim[i]) > 0:
            sim.insert(i, "1")
            sim.pop(i+1)
    
    h = ""
    for c in sim:
        h += c
    #print(h)
    
    del shingles[:]
    
    return h
    
def sort(similarity):
    print("sorting...")
    for j in range(0, len(similarity)):
        for i in range(1, len(similarity)):
            #print(similarity)
            if similarity[i-1][1] < similarity[i][1]:
                #print("swap-" + str(i-1) + "-" + str(i))
                similarity[i-1], similarity[i] = similarity[i], similarity[i-1]
                
def createHashFile(similarity):
    for i in range(0, len(similarity)):
        newFile.write(similarity[i][0] + "\n")
        newFile.write(str(similarity[i][1]) + "\n")
        newFile.write(str(similarity[i][2]) + "\n")
        newFile.write(str(similarity[i][3]) + "\n")

def hamming(bin1, bin2):
    ham = 0
    #print(bin1 + "---" + bin2)
    for i in range(0, len(bin1)):
        if bin1[i]!=bin2[i]:
            ham+=1
    return ham

print("reading...")
for line in warc:
    if line.startswith("<source>"):
        #print(line.find("</location>"))
        loc = line[18:line.find("</location>")]
        stopwords = open("stopwords.txt", "r").read().split('\n')
        for stopword in stopwords:
            text = text.replace(" " + stopword + " ", " ")
            text = text.replace("\n" + stopword + " ", " ")
            text = text.replace(" ", "")
        
        for i in range(0, len(text)):
            text = text.strip()
            shingles.append(text[i:i+10])
            #print(text[i:i+6])
        
        #print(shingles)
        print(d)
        d+=1
        sim = getSim(shingles)
        similarity = similarity + [(prevLoc, sim, int(sim,2), "")]
        #print(prevLoc)
        #print(sim)
        prevSim = sim
        prevLoc = loc
        
        
        #print(text)
        text = ""
    if not line.startswith("<source>"):
        line = line.lower()
        text = text + line
 
sort(similarity)
print(similarity)
for i in range(1, len(similarity)):
    print(i)
    simH = ((similarity[i][0], similarity[i][1], similarity[i][2], hamming(similarity[i-1][1], similarity[i][1])))
    #print(simH)
    similarity.pop(i)
    similarity.insert(i, simH)
    print(similarity)
    
createHashFile(similarity)

newFile.close()
warc.close()
