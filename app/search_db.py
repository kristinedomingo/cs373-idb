import re
from db import db 
from models import Artist, Track, Album
import collections

def search_db(type, word):
	words=re.split(' ', word)
	artists= Artist.query.all()
	tracks = Track.query.all()
	albums = Album.query.all()
	ors ={}
	ands=[]

	for word in words:
		print("******")
		print(word)
		print("****|\n")
		if word not in ors:
			ors[word]={}
		if 'artists' not in ors[word]:
			ors[word]['artists']=[]
		if 'tracks' not in ors[word]:
			ors[word]['tracks']=[]
		if 'albums' not in ors[word]:
			ors[word]['albums']=[]	
		for artist in artists:
			x=find_word_artist(word, artist)
			
			if x != -1:
				ors[word]['artists'].append(artist)
				print (artist)
		for track in tracks:
			x=find_word_track(word, track)
			if x != -1:
				ors[word]['tracks'].append(track)
				print (track)
		for album in albums:
			x=find_word_album(word, album)
			if x != -1:
				ors[word]['albums'].append(album)
				print (album)
	and_words= iter(words)
	search_and=ors[next(and_words)]
	temp={}
	
	for word in and_words:
		temp['artists']=[]
		temp['tracks']=[]
		temp['albums']=[]
		for model in search_and:
			for data in search_and[model]:
				if model == 'artists':
					x=find_word_artist(word, data)
					print(data)
					if x != -1:
						temp['artists'].append(data)
						#print (artist)
				if model == 'tracks':
					print(data)
					x=find_word_track(word, data)
					if x != -1:
						temp['tracks'].append(data)
						print (track)
				if model == 'albums':
					print(data)
					x=find_word_album(word, data)
					if x != -1:
						temp['albums'].append(data)
						#print (album)
		search_and=temp

	#print(search_and)
	return ors
	
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
	combo=collections.OrderedDict()

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
