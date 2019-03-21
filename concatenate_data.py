import os, re

directory = "test_data/"

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
    data = data.replace(']', ' ]')
    
    components = data.split('[')
    
    for i in components:
        if i.split(" ")[0] == "Chorus" and chorus == "":
            chorus = i.split("]")[1]
        
        elif i.split(" ")[0] == "Verse":
            verses.append(i.split("]")[1])
        
        elif i.split(" ")[0] == "Bridge":
            bridges.append(i.split("]")[1])
        
        elif i.split(" ")[0] == "Pre-Chorus":
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

def add_to_corpus(corpus, toAdd):
    
    data = prepare_chars(data)
    
    if len(data) > 0:
        corpus.write(data + '\n\n')

chorusCorpus = open('corpus_chorus.lyc', 'w')
prechorusCorpus = open('corpus_prechorus.lyc', 'w')
verseCorpus = open('corpus_verse.lyc', 'w')
bridgeCorpus = open('corpus_bridge.lyc', 'w')

total = len(os.listdir(directory))
count = 1

for filename in os.listdir(directory):
	print("Adding " + str(count) + '/' + str(total) + " to corpus", end='\r')
	f = open("test_data/" + filename, 'r')
	data = clear_whitelines(f.read())
    
	if data.count('\n') >= 14:
        
        chorus, prechorus, verses, bridges = split_components(data)
        
        add_to_corpus(chorusCorpus, chorus)
        add_to_corpus(prechorusCorpus, prechorus)
        for data in verses:
            add_to_corpus(verseCorpus, data)
        for data in bridges:
            add_to_corpus(bridgeCorpus, data)
            
        
	f.close()
	count += 1

chorusCorpus.close()
prechorusCorpus.close()
verseCorpus.close()
bridgeCorpus.close()
print("\nCorpus complete" + ' ' * 100)