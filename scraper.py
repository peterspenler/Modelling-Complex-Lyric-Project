import requests, json, sys, os
from bs4 import BeautifulSoup
from key import token

# This script is based off of the lyric stripping code from
# https://dev.to/willamesoares/how-to-integrate-spotify-and-genius-api-to-easily-crawl-song-lyrics-with-python-4o62 

################## READ ME #############################
# To use this script you need to get a genius API key  #
# and put it in a new file "key.py" assigned to 'token'#
########################################################

data_dir = 'test_data/'

# Missing brackets in the exclusors list are intentional
exclusors = ['booklet', 
			'credits',
			'instrumental',
			'[tracklist+albumart]', 
			'tracklist', 
			'[albumart]', 
			'q&a', 
			'[artwork]', 
			'skit', 
			'remix)', 
			'[setlist]',
			'[setlists]', 
			'demo)',
			'demo]',
			'[live',
			'(live',
			'interview',
			'tourdates']

def request_song_info(song_artist):
	base_url = 'https://api.genius.com'
	headers = {'Authorization': 'Bearer ' + token}
	search_url = base_url + '/search'
	data = {'q': song_artist}
	response = requests.get(search_url, data=data, headers=headers)

	json = response.json()
	remote_song_info = None

	for hit in json['response']['hits']:
		if song_artist.lower() in hit['result']['primary_artist']['name'].lower():
			remote_song_info = hit
			break

	if remote_song_info == None:
		try:
			remote_song_info = json['response']['hits'][0]
		except:
			remote_song_info = None
	if remote_song_info != None:
		print("Found Artist: " + remote_song_info['result']['primary_artist']['name'] + ", ID: " + str(remote_song_info['result']['primary_artist']['id']))

		text = input("Is this correct? (y/n): ")
		if text.lower() == 'y':
			return remote_song_info['result']['primary_artist']['id']
		elif text.lower() == 'n':
			return -1
		else:
			print("assuming no")
			return -1

		return -2
	else:
		print("Artist not found")
		return -3


def request_artist_songs(artist_num, num, page):
	base_url = 'https://api.genius.com'
	headers = {'Authorization': 'Bearer ' + token}
	search_url = base_url + '/artists/' + artist_num + '/songs'
	data = {'per_page': num, 'page': page}
	response = requests.get(search_url, data=data, headers=headers)

	json = response.json()

	if json['meta']['status'] != 200:
		print(json)
		return None, False

	if json['response']['next_page'] == None:
		return json['response']['songs'], False

	return json['response']['songs'], True


def lyrics_from_hit(hit):
	if hit:
		title = hit['full_title'].lower().replace(" ", "")
		if not any(x in title for x in exclusors):
			try:
				song_url = hit['url']
				page = requests.get(song_url)
				html = BeautifulSoup(page.text, 'html.parser')
				lyrics = html.find('div', class_='lyrics').get_text()

				return lyrics

			except:
				return None

	else:
		return ''

def save_lyrics(lyrics, filename, hit):
	if not os.path.exists(data_dir):
    		os.makedirs(data_dir)
	f = open( data_dir + filename, 'w')
	#f.write(json.dumps(hit))
	#f.write('\n-----------\n')
	f.write(lyrics)
	f.close()
	print("Wrote " + filename)

artists = []

if len(sys.argv) < 2:
	print('Takes 1 argument, received ' + str(len(sys.argv) - 1))
	sys.exit()

for i in range(1,len(sys.argv)):
	print("Searching for artist '" + sys.argv[i] + "'")
	song = request_song_info(sys.argv[i])
	if song >= 0:
		artists.append(song)

for id in artists:
	page = 1
	while True:
		songs, next_page = request_artist_songs(str(id), '20', page)

		if songs != None:
			for hit in songs:
				if hit['primary_artist']['id'] == id:
					lyrics = lyrics_from_hit(hit)
					if lyrics != None and lyrics != '':
						save_lyrics(lyrics, hit['full_title'][:50].replace('/', '') + '.lyc', hit)
		else:
			print("Encountered an error")
			break
		if not next_page:
			break

		page += 1

print("All songs written")