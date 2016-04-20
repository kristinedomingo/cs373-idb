import re
from db import db 
from models import Artist, Track, Album
import collections

def search_db(word):
	words=re.split(' ', word)
	artists= Artist.query.all()
	tracks = Track.query.all()
	albums = Album.query.all()
	ors ={}
	ands=[]
	tempors={}
	for word in words:
		if word not in ors:
			ors[word]={}
			tempors[word]={}
		if 'artists' not in ors[word]:
			ors[word]['artists']=[]
			tempors[word]['artist']=[]
		if 'tracks' not in ors[word]:
			ors[word]['tracks']=[]
			tempors[word]['tracks']=[]
		if 'albums' not in ors[word]:
			ors[word]['albums']=[]	
			tempors[word]['albums']=[]	
		for artist in artists:
			x=find_word_artist(word, artist)
			
			if x != -1:
				tempors[word]['artist'].append(artist)
				ors[word]['artists'].append({'name': artist.name, 'img': artist.col_img, 'id': artist.spotify_id})
				print (artist)
		for track in tracks:
			x=find_word_track(word, track)
			if x != -1:
				tempors[word]['tracks'].append(track)
				ors[word]['tracks'].append({'name': track.title, 'img': track.col_img, 'id': track.spotify_id})
				print (track)
		for album in albums:

			x=find_word_album(word, album)
			if x != -1:
				tempors[word]['albums'].append(album)
				ors[word]['albums'].append({'name': album.name, 'img': album.col_img, 'id': album.spotify_id})
				print (album)
	and_words= iter(words)
	next_w=next(and_words)
	search_and=tempors[next_w]
	json_and=ors[next_w]
	temp={}
	temp2={}
	
	for word in and_words:
		temp['artists']=[]
		temp['tracks']=[]
		temp['albums']=[]
		temp2['artists']=[]
		temp2['tracks']=[]
		temp2['albums']=[]
		for model in search_and:
			for data in search_and[model]:
				if model == 'artists':
					x=find_word_artist(word, data)
					print(data)
					if x != -1:
						temp['artists'].append(data)
						temp2['artist'].append(json_and[model])
						#print (artist)
				if model == 'tracks':
					print(data)
					x=find_word_track(word, data)
					if x != -1:
						temp['tracks'].append(data)
						temp2['tracks'].append(json_and[model])
						print (track)
				if model == 'albums':
					print(data)
					x=find_word_album(word, data)
					if x != -1:
						temp['albums'].append(data)
						temp2['albums'].append(json_and[model])
						#print (album)
		search_and=temp

	#print(search_and)
	json={'and':search_and, 'or':ors}
	return json
	
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
    search_db( "Kanye West")
