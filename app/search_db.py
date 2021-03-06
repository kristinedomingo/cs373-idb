import re
from db import db 
from models import Artist, Track, Album
import collections
#This is the search method for search bar the db

def search_db(word):
	words=re.split(' ', word)
	artists= Artist.query.all()
	tracks = Track.query.all()
	albums = Album.query.all()
	ors ={}
	ands={}
	ors['artists']=[]
	ands['artists']=[]

	ors['tracks']=[]
	ands['tracks']=[]

	ors['albums']=[]	
	ands['albums']=[]	

	#check to see if the artist has all the words in it if not check to see if atleast one them is in there
	for artist in artists:
		if all(find_word_artist(word,artist)!=-1 for word in words):
			context=bold_artist(artist,words)
			ands['artists'].append({'name': artist.name, 'img': artist.col_img, 'id': artist.spotify_id,'context':context})
		elif any(find_word_artist(word,artist)!=-1 for word in words):
			context=bold_artist(artist,words)
			ors['artists'].append({'name': artist.name, 'img': artist.col_img, 'id': artist.spotify_id,'context':context})
	#check to see if the track has all the words in it if not check to see if at least one them is in there
	for track in tracks:
		if all(find_word_track(word,track)!=-1 for word in words):

			context=bold_track(track,words)


			ands['tracks'].append({'name': track.title, 'img': track.col_img, 'id': track.spotify_id,'context':context})
		elif any(find_word_track(word,track)!=-1 for word in words):
		
			context=bold_track(track,words)
			ors['tracks'].append({'name': track.title, 'img': track.col_img, 'id': track.spotify_id,'context':context})
	#check to see if the track has all the words in it if not check to see if at least one them is in there
	for album in albums:
		if all(find_word_album(word,album)!=-1 for word in words):
			context=bold_album(album,words)
			ands['albums'].append({'name': album.name, 'img': album.col_img, 'id': album.spotify_id, 'context':context})
			
		elif any(find_word_album(word,album)!=-1 for word in words):
			context=bold_album(album,words)
			ors['albums'].append({'name': album.name, 'img': album.col_img, 'id': album.spotify_id, 'context':context})
	print(ors['tracks'])
	print("ANDDS")
	print(ands['tracks'])

	json={'and':ands, 'or':ors}
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
				s=s[0:x]+' <span class="context"> '+s[x:x+len(word)]+'</span>'+ s[x+len(word):len(s)]+' '
				counter=counter+1
		if counter ==0:
			detail=artist.name
			ld=detail.lower()
			x= ld.find(lw)
			if x != -1:
				s=s+"By: "+detail[0:x]+' <span class="context"> '+detail[x:x+len(word)]+'</span>'+ detail[x+len(word):len(detail)]+ ' '
				counter=counter+1
			detail=artist.recent_album
			ld=detail.lower()
			x= ld.find(lw)
			if x != -1 and counter==0:
				
				s=s+'Most Recent Album: '+detail[0:x]+' <span class="context"> '+detail[x:x+len(word)]+'</span>'+ detail[x+len(word):len(detail)]+' '
				counter=counter+1
			detail=artist.top_track
			ld=detail.lower()
			x= ld.find(lw)

			if x !=-1 and counter==0:
				

				s=s+'Top Track: '+detail[0:x]+' <span class="context"> '+detail[x:x+len(word)]+'</span>'+ detail[x+len(word):len(detail)]+' '

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
				s=s[0:x]+' <span class="context"> '+s[x:x+len(word)]+'</span>'+ s[x+len(word):len(s)]+' '
				counter=counter+1
		
		if counter==0:
			detail=track.title
			ld=detail.lower()
			x= ld.find(lw)
			if x != -1:
				s=s+detail[0:x]+' <span class="context"> '+detail[x:x+len(word)]+'</span>'+ detail[x+len(word):len(detail)]+' '
				counter=counter+1
			detail=track.artist_name
			ld=detail.lower()
			x= ld.find(lw)
			if x != -1 and counter==0:
				
				s=s+'By: '+detail[0:x]+' <span class="context"> '+detail[x:x+len(word)]+'</span>'+ detail[x+len(word):len(detail)]+' '
				counter=counter+1
			detail=track.album
			ld=detail.lower()
			x= ld.find(lw)
			if x !=-1 and counter==0:
				

				s=s+'Album: '+detail[0:x]+' <span class="context"> '+detail[x:x+len(word)]+'</span>'+ detail[x+len(word):len(detail)]+' '
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
				s=s[0:x]+' <span class="context"> '+s[x:x+len(word)]+'</span>'+ s[x+len(word):len(s)]+' '
				counter=counter+1
		if counter==0:
			detail=album.name
			ld=detail.lower()
			x= ld.find(lw)
			if x != -1 and counter==0:
				s=s+"Album : "+detail[0:x]+' <span class="context"> '+detail[x:x+len(word)]+'</span>'+ detail[x+len(word):len(detail)]+' '
				counter=counter+1
			detail=album.artist_name
			ld=detail.lower()
			x= ld.find(lw)
			if x != -1 and counter==0:
				
				s=s+'By : '+detail[0:x]+' <span class="context"> '+detail[x:x+len(word)]+'</span>'+ detail[x+len(word):len(detail)]+' '
				counter=counter+1
			detail=album.release_date
			ld=detail.lower()
			x= ld.find(lw)
			if x !=-1 and counter==0:
				
				counter=counter+1
				s=s+'Release : '+detail[0:x]+' <span class="context"> '+detail[x:x+len(word)]+'</span>'+ detail[x+len(word):len(detail)]+' '
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

if __name__ == "__main__":
	search_db( 'Guard')

