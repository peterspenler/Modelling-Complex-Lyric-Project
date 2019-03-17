import os, re

directory = "test_data/"

def clear_whitelines(data):
	result = data
	while '\n\n' in result:
		result = result.replace('\n\n', '\n')
	result = result.strip()
	return result

def prepare_chars(data):
    result = data
    result = result.replace('\n', ' \n ')
    result = result.replace(',', ' ,')
    
    #remove characters that are not: alphanumeric, comma, apostrophe space, newline
    result = [c for c in result if c.isalpha() or c == "'" or c == '\n' or c == " "or c == ","]
    result = ''.join(result)
    
    return result

corpus = open('corpus.lyc', 'w')

total = len(os.listdir(directory))
count = 1

for filename in os.listdir(directory):
	print("Adding " + str(count) + '/' + str(total) + " to corpus", end='\r')
	f = open("test_data/" + filename, 'r')
	data = clear_whitelines(f.read())
    data = prepare_chars(data)
	if data.count('\n') >= 14:
		corpus.write(data + '\n\n')
	f.close()
	count += 1

corpus.close()
print("\nCorpus complete" + ' ' * 100)