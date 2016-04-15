import re
from db import db 
from models import Artist, Track, Album

def search_db(type, word):
	words=re.split(' ', word)
	artists= Artist.query.all()
	tracks = Track.query.all()
	albums = Album.query.all()
	items ={}
	combo= combo_words(words)

	for i in combo:
		items[i]=[]
		for word in combo[i]:
			print("******")
			print(word)
			print("****|\n")
			for artist in artists:
				x=find_word_artist(word, artist)
				if x != -1:
					items[i].append(artist)
					print (artist)
			for track in tracks:
				x=find_word_track(word, track)
				if x != -1:
					items[i].append(track)
					print (track)
			for album in albums:
				x=find_word_album(word, album)
				if x != -1:
					items[i].append(album)
					print (album)
	return items
def find_word_artist(word, artist):
	x=artist.name.find(word)
	if x !=-1:
		return x
	x= artist.recent_album.find(word)
	if x !=-1:
		return x
	x= artist.top_track.find(word)

	if x !=-1:
		return x
	return x

def find_word_album(word, album):
	x= album.name.find(word)
	if x != -1:
		return x
	x= album.artist_name.find(word)
	if x !=-1:
		return x
	x= album.release_date.find(word)
	if x !=-1:
		return x
	tracks= Track.query.filter(Track.album_id == album.id).all()
	for track in tracks:
		x= find_word_track(word, track)
		if x!=-1:
			return x
	return x

def find_word_track(word, track):
	x= track.title.find(word)
	if x !=-1:
		return x
	x= track.artist_name.find(word)
	if  x!=-1:
		return x
	x= track.album.find(word)
	if x !=-1:
		return x
	return x
def combo_words(words):
	combo={}

	for i in range(0, len(words)):
		string=''
		count =0
		for j in range(i, len(words)):
			if count !=0:
				string+=' '
			string+=words[j]
			count= count +1
			if count not in combo:
				combo[count]=[]
			combo[count].append(string)
	print(combo)
	return combo

if __name__ == "__main__":
    search_db("all", "Kanye West")
