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
			tempors[word]['artists']=[]
		if 'tracks' not in ors[word]:
			ors[word]['tracks']=[]
			tempors[word]['tracks']=[]
		if 'albums' not in ors[word]:
			ors[word]['albums']=[]	
			tempors[word]['albums']=[]	
		for artist in artists:
			x=find_word_artist(word, artist)
			
			if x != -1:
				tempors[word]['artists'].append(artist)
				context=bold_artist(artist,[word])
				ors[word]['artists'].append({'name': artist.name, 'img': artist.col_img, 'id': artist.spotify_id,'context':context})
		for track in tracks:
			x=find_word_track(word, track)
			if x != -1:

				tempors[word]['tracks'].append(track)
				context=bold_track(track,[word])
				ors[word]['tracks'].append({'name': track.title, 'img': track.col_img, 'id': track.spotify_id,'context':context})
		for album in albums:

			x=find_word_album(word, album)
			if x != -1:
				tempors[word]['albums'].append(album)
				context=bold_album(album,[word])
				ors[word]['albums'].append({'name': album.name, 'img': album.col_img, 'id': album.spotify_id, 'context':context})
	and_words= iter(words)
	next_w=next(and_words)
	search_and=tempors[next_w]
	json_and=ors[next_w]
	temp={}
	temp2={}
	print(ors)
	print("ASDFASDFASDFASDFADF")
	for word in and_words:
		print(word)
		temp['artists']=[]
		temp['tracks']=[]
		temp['albums']=[]
		temp2['artists']=[]
		temp2['tracks']=[]
		temp2['albums']=[]
		for model in search_and:
			for data,json in zip(search_and[model],json_and[model]):
				if model == 'artists':
					x=find_word_artist(word, data)
					
					if x != -1:
						print(data)
						temp['artists'].append(data)

						temp2['artists'].append(json)
						#print (artist)
				if model == 'tracks':
					
					x=find_word_track(word, data)
					if x != -1:
						print(data)
						temp['tracks'].append(data)
						temp2['tracks'].append(json)
						print (track)
				if model == 'albums':
					x=find_word_album(word, data)
					if x != -1:
						print(data)
						temp['albums'].append(data)
						temp2['albums'].append(json)
						#print (album)
		search_and=temp.copy()
		json_and=temp2.copy()

	for model in search_and:
		for data,json in zip(search_and[model],json_and[model]):
			if model == 'artists':
				json['context']=bold_artist(data, words)
				print(json['context'])
			if model == 'tracks':
				json['context']=bold_track(data,words)
				print(json['context'])
			if model == 'albums':
				json['context']=bold_album(data,words)
				print(json['context'])
	print(json_and)
	print(ors)

	json={'and':json_and, 'or':ors}
	return json
	
def find_word_artist(word, artist):
	s=artist.name.lower()
	lw=word.lower()
	x=s.find(word.lower())
	if x !=-1:
		return x
	s=artist.recent_album.lower()
	x= s.find(lw)
	if x !=-1:
		return x
	s=artist.top_track.lower()
	x= s.find(lw)
	if x !=-1:
		return x
	return x

def find_word_album(word, album):
	s= album.name.lower()
	lw=word.lower()
	x= s.find(lw)
	if x != -1:
		return x
	s=album.artist_name.lower()
	x= s.find(lw)
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
	lw=word.lower()
	s= track.title.lower()
	x= s.find(lw)
	if x !=-1:
		return x
	s= track.artist_name.lower()
	x= s.find(lw)

	if  x!=-1:
		return x
	s=track.album.lower()

	x= s.find(lw)
	if x !=-1:
		return x
	return x
def bold_artist(artist, words):
	s=''
	x=-1
	counter=0
	for word in words:
		lw=word.lower()
		if len(s)!=0:
			ls=s.lower()
			x=ls.find(lw)
			if x!=-1:
				s=s[0:x]+' <span class="context"> '+s[x:x+len(word)]+'</span>'+ s[x+len(word):len(s)]
				counter=counter+1
		if counter ==0:
			detail=artist.name
			ld=detail.lower()
			x= ld.find(lw)
			if x != -1:
				s=s+"By: "+detail[0:x]+' <span class="context"> '+detail[x:x+len(word)]+'</span>'+ detail[x+len(word):len(detail)]
				counter=counter+1
			detail=artist.recent_album
			ld=detail.lower()
			x= ld.find(lw)
			if x != -1 and counter==0:
				
				s=s+'Most Recent Album: '+detail[0:x]+' <span class="context"> '+detail[x:x+len(word)]+'</span>'+ detail[x+len(word):len(detail)]
				counter=counter+1
			detail=artist.top_track
			ld=detail.lower()
			x= ld.find(lw)

			if x !=-1 and counter==0:
				

				s=s+'Top Track: '+detail[0:x]+' <span class="context"> '+detail[x:x+len(word)]+'</span>'+ detail[x+len(word):len(detail)]

		counter=0
		

	return s
def bold_track(track, words):
	s=''
	counter=0
	x=-1
	for word in words:
		lw=word.lower()
		if len(s)!=0:
			ls=s.lower()
			x=ls.find(lw)
			if x!=-1:
				s=s[0:x]+' <span class="context"> '+s[x:x+len(word)]+'</span>'+ s[x+len(word):len(s)]
				counter=counter+1
		
		if counter==0:
			detail=track.title
			ld=detail.lower()
			x= ld.find(lw)
			if x != -1:
				s=s+detail[0:x]+' <span class="context"> '+detail[x:x+len(word)]+'</span>'+ detail[x+len(word):len(detail)]
				counter=counter+1
			detail=track.artist_name
			ld=detail.lower()
			x= ld.find(lw)
			if x != -1 and counter==0:
				
				s=s+'By: '+detail[0:x]+' <span class="context"> '+detail[x:x+len(word)]+'</span>'+ detail[x+len(word):len(detail)]
				counter=counter+1
			detail=track.album
			ld=detail.lower()
			x= ld.find(lw)
			if x !=-1 and counter==0:
				

				s=s+'Album: '+detail[0:x]+' <span class="context"> '+detail[x:x+len(word)]+'</span>'+ detail[x+len(word):len(detail)]
				counter=counter+1
		counter=0
	return s

def bold_album(album, words):
	s=''
	counter=0
	x=-1
	for word in words:
		lw=word.lower()
		if len(s)!=0:
			ls=s.lower()
			x=ls.find(lw)
			if x!=-1:
				s=s[0:x]+' <span class="context"> '+s[x:x+len(word)]+'</span>'+ s[x+len(word):len(s)]
				counter=counter+1
		if counter==0:
			detail=album.name
			ld=detail.lower()
			x= ld.find(lw)
			if x != -1 and counter==0:
				s=s+"Album : "+detail[0:x]+' <span class="context"> '+detail[x:x+len(word)]+'</span>'+ detail[x+len(word):len(detail)]
				counter=counter+1
			detail=album.artist_name
			ld=detail.lower()
			x= ld.find(lw)
			if x != -1 and counter==0:
				
				s=s+'By : '+detail[0:x]+' <span class="context"> '+detail[x:x+len(word)]+'</span>'+ detail[x+len(word):len(detail)]
				counter=counter+1
			detail=album.release_date
			ld=detail.lower()
			x= ld.find(lw)
			if x !=-1 and counter==0:
				
				counter=counter+1
				s=s+'Release : '+detail[0:x]+' <span class="context"> '+detail[x:x+len(word)]+'</span>'+ detail[x+len(word):len(detail)]
				counter=counter+1
			if counter==0:
				tracks=Track.query.filter(Track.album_id== album.id).all()
				for track in tracks:
					x=find_word_track(word,track)
					if x!=-1 and counter==0:
						s=s+bold_track(track,[word])
						counter=counter+1
		counter=0
	return s
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
def s():
	s="1 2 3 4 5"
	w=re.split(' ',s)
	return w
if __name__ == "__main__":
	search_db( 'Wolves')

