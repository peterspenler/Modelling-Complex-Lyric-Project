import os, re

directory = "test_data/"
write_dir = "data/"

def clear_whitelines(data):
	result = data
	while '\n\n' in result:
		result = result.replace('\n\n', '\n')
	result = result.strip()
	return result

def split_components(data):
    
    verses = []
    bridges = []
    chorus = ""
    prechorus = ""
    
    #this will help us identify the song component
    data = data.replace('[?]', '').replace("(Hook)", "[Hook]").replace("(Chorus)", "[Chorus]").replace("(hook)", "[hook]").replace("(chorus)", "[chorus]").replace(']', ' ]')
    
    components = data.split('[')

    #if components
    
    for i in components:
        j = i.split("]")
        if len(j[0]) < 70:
            if (("chorus" in j[0].lower()) or ("hook" in j[0].lower())) and (chorus == "") and (len(j) > 1):
                print("HIT")
                chorus = j[1]
        
            elif "verse" in j[0].lower() and (len(j) > 1):
                verses.append(j[1])
        
            elif "bridge" in j[0].lower() and (len(j) > 1):
                bridges.append(j[1])
        
            elif "pre-chorus" in j[0].lower() or "pre chorus" in j[0].lower() and (len(j) > 1):
                prechorus = i.split("]")[1]
    
    return chorus, prechorus, verses, bridges

def prepare_chars(data):
    result = data
    result = result.replace('\n', ' \n ')
    result = result.replace(',', ' ,')
    
    #remove characters that are not: alphanumeric, comma, apostrophe space, newline
    result = [c for c in result if c.isalpha() or c == "'" or c == '\n' or c == " "or c == ","]
    result = ''.join(result)
    
    return result

def add_to_corpus(type, toAdd, count):
    
    data = prepare_chars(toAdd)
    
    if len(toAdd) > 0:
        if not os.path.exists(write_dir + type + "/"):
            os.makedirs(write_dir + type + "/")
        corpus = open(write_dir + type + "/data_" + str(count) + ".lyc", 'w')
        corpus.write(toAdd.strip())
        corpus.close()
        return 1
    else:
        return 0

chorusC = 0
prechorusC = 0
verseC = 0
bridgeC = 0


total = len(os.listdir(directory))
count = 1

for filename in os.listdir(directory):
	print("Adding " + str(count) + '/' + str(total) + " to corpus" + filename, end='\n')
	f = open("test_data/" + filename, 'r')
	data = clear_whitelines(f.read())
    
	if data.count('\n') >= 14:
        
		chorus, prechorus, verses, bridges = split_components(data)
		
		chorusC += add_to_corpus("chorus", chorus, chorusC)
		prechorusC += add_to_corpus("prechorus", prechorus, prechorusC)
		for verse in verses:
		    verseC += add_to_corpus("verse", verse, verseC)
		for bridge in bridges:
		    bridgeC += add_to_corpus("bridge", bridge, bridgeC)
		    
		
	f.close()
	count += 1

print("\nCorpus complete" + ' ' * 100)
