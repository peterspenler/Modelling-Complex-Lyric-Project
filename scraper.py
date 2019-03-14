import requests, json, sys
from bs4 import BeautifulSoup

# This script is based off of the lyric stripping code from
# https://dev.to/willamesoares/how-to-integrate-spotify-and-genius-api-to-easily-crawl-song-lyrics-with-python-4o62 

token = 'AslLhrQhDquWv_R-OToQZ_DrzkbgR01c5yI448peiQ9puaKB7c22BU4_9w_XosIX'

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

def request_song_info(song_title, song_artist):
	base_url = 'https://api.genius.com'
	headers = {'Authorization': 'Bearer ' + token}
	search_url = base_url + '/search'
	data = {'q': song_title + ' ' + song_artist}
	response = requests.get(search_url, data=data, headers=headers)

	json = response.json()
	remote_song_info = None

	for hit in json['response']['hits']:
		if song_artist.lower() in hit['result']['primary_artist']['name'].lower():
			remote_song_info = hit
			break

	print("Found Artist: " + remote_song_info['result']['primary_artist']['name'] + ", ID: " + str(remote_song_info['result']['primary_artist']['id']))

	return remote_song_info


def request_artist_songs(artist_num, num, page):
	base_url = 'https://api.genius.com'
	headers = {'Authorization': 'Bearer ' + token}
	search_url = base_url + '/artists/' + artist_num + '/songs'
	data = {'per_page': num, 'page': page}
	response = requests.get(search_url, data=data, headers=headers)

	json = response.json()

	if json['meta']['status'] != 200:
		print(json)
		return None

	if json['response']['next_page'] == None:
		print('All songs saved')
		return None

	return json['response']['songs']


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
	f = open( 'test_data/' + filename, 'w')
	#f.write(json.dumps(hit))
	#f.write('\n-----------\n')
	f.write(lyrics)
	f.close()
	print("Wrote " + filename)


if len(sys.argv) != 2:
	print('Takes 1 argument, received ' + str(len(sys.argv) - 1))
	sys.exit()

print("Searching for artist '" + sys.argv[1] + "'")
song = request_song_info('', sys.argv[1])
id = song['result']['primary_artist']['id']

page = 1

while True:
	songs = request_artist_songs(str(id), '50', page)

	if songs != None:
		for hit in songs:
			if hit['primary_artist']['id'] == id:
				lyrics = lyrics_from_hit(hit)
				if lyrics != None and lyrics != '':
					save_lyrics(lyrics, hit['full_title'][:50].replace('/', '') + '.lyc', hit)
	else:
		break

	page += 1