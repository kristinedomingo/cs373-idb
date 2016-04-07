#!flask/bin/python
from models import Artist, Track, Album
import requests
import spotipy
import spotipy.util as util
from db import db 
import json
import os.path
import re
from datetime import timedelta
# from scraper import scrappy, get_artist_scrape, get_album_scrape, get_tracks_scrape


def create_artist(artist_json):

	count =0
	count2=0
	for artist in artist_json['artists']:
		top_track=''
		if 'top_track' in artist:
			top_track=artist['top_track']['name']
		if 'col_img' in artist:
			artist_model=Artist(artist['name'],artist['num_albums'],artist['last_album']['name'],top_track,artist['popularity'],artist['uri'],artist['id'],artist['images'][1]['url'], artist['col_img'],artist['followers']['total'])
		db.session.add(artist_model)
		db.session.commit()
		count2=count+1
	print ('\ntotal_top:')
	print(count)
	print('\nartist')
	print(count2)


def create_album(album_json):
	for album in album_json['albums']:
		#print(album['name'])
		artist=Artist.query.filter(Artist.name==album['artist_name']).first()
		if artist ==None:
			i=0
		else:
			album_model= Album(album['name'],album['artist_name'], album['release_date'],album['length'],album['num_tracks'],album['uri'],album['id'],album['images'][1]['url'],album['col_img'], album['href'])
		
			album_model.artists.append(artist)
			db.session.add(album_model)
			db.session.commit()

def create_tracks(track_json):
	
	for track in track_json['tracks']:
		#print(track['name'])
		album_id=None
		album= Album.query.filter(Album.name ==track['album_name']).first()
		artist_in_track= re.split(', ',track['artist_name'])
		
		if album == None:
			album_id=None
		else:
			album_id=album.id
		#print(Album.query.all())
			
		tracks_model= Track(track['name'],track['artist_name'],track['release_date'],track['album_name'],track['album']['images'][1]['url'],track['duration_ms'],track['uri'],track['id'],album_id,track['col_img'],track['href'])
		
		for art_tr in artist_in_track:
			
				artist= Artist.query.filter(Artist.name == art_tr).first()
				if artist== None:
					i=1
				else:	
					tracks_model.artists2.append(artist)
		db.session.add(tracks_model)
		db.session.commit()

def create_tracks_album(album_json):
	for album in album_json['albums']:
		album_db= Album.query.filter(Album.name== album['name']).first()
		if album_db == None:
			i=1
		else:
			for track in album['tracks']['items']:
				artist_name=''
				count=0
				for artist in track['artists']:
					if count >=1:
						artist_name+=', '
					artist_name+=artist['name']
					count=count+1
				track_exist= Track.query.filter(Track.title == track['name']).first()
				if track_exist ==None:
					track['name']
					tracks_model=Track(track['name'],artist_name,album_db.release_date,album_db.name,album_db.images,track['duration_ms'],track['uri'],track['id'],album_db.id,album_db.col_img,track['href'])
					artist_in_track= re.split(', ', artist_name)
					for art_tr in artist_in_track:
						artist= Artist.query.filter(Artist.name == art_tr).first()
						if artist ==None:
							i=1
						else:
							tracks_model.artists2.append(artist)
					db.session.add(tracks_model)
					db.session.commit()
				
def add_track(trackid):
	track = requests.get('https://api.spotify.com/v1/tracks/' + trackid).json()
	trackdb = Track.query.filter(track['name'] == Track.title).first()
	if trackdb == None:

#Get track album cover
		if track["album"]["images"]:
			track["col_img"] = track["album"]["images"][len(track["album"]["images"]) - 1]["url"]

		# Get artist(s), and add to artist queue
		names = ""
		for artist in track["artists"]:
			names += artist["name"] + ', '
	

# Get associated album
		track["album_name"] = track["album"]["name"]

		# Get release date from album
		album_href = track["album"]["href"]
		album_json = requests.get(album_href).json()
		track["release_date"] = album_json["release_date"]

		# Get track duration
		duration = timedelta(milliseconds = track["duration_ms"])
		minutes = str(duration.seconds // 60)
		seconds = str(duration.seconds % 60).zfill(2)
		track["duration"] = minutes + ":" + seconds

# Delete information that is not going to be used
# Add completed track information to json
		album = Album.query.filter(Album.name == track['album_name']).first()
		if album == None:
			album_id = None
		else:
			album_id = album.id

		tracks_model= Track(track['name'],names,track['release_date'],track['album_name'],track['album']['images'][1]['url'],track['duration_ms'],track['uri'],track['id'],album_id,track['col_img'],track['href'])
		for artist in track["artists"]:
			artistdb = Artist.query.filter(Artist.name == artist["name"]).first()
			if artistdb == None:
				pass
			else:
				tracks_model.artists2.append(artistdb)
		db.session.add(tracks_model)
		db.session.commit()

def add_artist(artistid):
	this_artist = requests.get('https://api.spotify.com/v1/artists/' + artistid).json()
	artistdb = Artist.query.filter(this_artist["name"] == Artist.name).first()
	if artistdb == None:

# Get and add the top track, and add track to queue
		top_tracks = requests.get(this_artist["href"] + '/top-tracks?country=US').json()["tracks"]
		if top_tracks:
			this_artist["top_track"] = {"name" : top_tracks[0]["name"], "id" : top_tracks[0]["id"]}
			add_track(this_artist["top_track"]["id"])

		# Get and add most recent album, and add album to queue
		albums = requests.get(this_artist["href"] + '/albums').json()["items"]
		last_album = albums[0]["name"]
		this_artist["last_album"] = {"name":last_album, "id": albums[0]["id"]}
		

#    if albums[0]["id"] not in scraped_albums and len(scraped_albums) < 250:
#       scraped_albums.append(albums[0]["id"])
#      albums_queue.append(albums[0]["id"])

# Add extra information (number of albums, album cover)
		this_artist["num_albums"] = len(albums)
		if this_artist["images"]:
			this_artist["col_img"] = this_artist["images"][len(this_artist["images"]) - 1]["url"]

		artist_model=Artist(this_artist['name'],this_artist['num_albums'],last_album,this_artist['top_track']['name'],this_artist['popularity'],this_artist['uri'],this_artist['id'],this_artist['images'][1]['url'], this_artist['col_img'],this_artist['followers']['total'])
		db.session.add(artist_model)
		db.session.commit()
		add_album(this_artist['last_album']['id'])

def add_album(albumid):
	this_album = requests.get('https://api.spotify.com/v1/albums/' + albumid).json()
	albumdb = Album.query.filter(this_album["name"] == Album.name).first()
	if albumdb == None:


		# Get album cover
		this_album["col_img"] = this_album["images"][len(this_album["images"]) - 1]["url"]

		# Get artist(s), and add to artists queue
		names = ""
		for artist in this_album["artists"]:
			names += artist["name"] + ', '
			add_artist(artist["id"])
		#if artist["id"] not in scraped_artists and len(scraped_artists) < 200:
		#   scraped_artists.append(artist["id"])
		#  artists_queue.append(artist["id"])
		this_album["artist_name"] = names.rstrip(', ')

		# Get number of tracks
		this_album["num_tracks"] = len(this_album["tracks"]["items"])

		# Get length (duration) of album
		duration_ms = 0
		for track in this_album["tracks"]["items"]:
			duration_ms += track["duration_ms"]

			duration = timedelta(milliseconds = duration_ms)

		# Convert milliseconds to a human-readable time
		minutes = str(duration.seconds // 60)
		seconds = str(duration.seconds % 60).zfill(2)
		this_album["length"] = minutes + ":" + seconds

		# Add tracks to tracks queue
		
		# if track["id"] not in scraped_tracks and len(scraped_tracks) < 350:
		#    scraped_tracks.append(track["id"])
		#   tracks_queue.append(track["id"])
		album_model= Album(this_album['name'],this_album['artist_name'], this_album['release_date'],this_album['length'],this_album['num_tracks'],this_album['uri'],this_album['id'],this_album['images'][1]['url'],this_album['col_img'], this_album['href'])
		artists = Artist.query.filter(Artist.name == this_album['artist_name']).first()
		if artists == None:
			pass
		else:
			album_model.artists.append(artists)

		# Add completed album information to json
		#albums_json["albums"].append(this_album)
		db.session.add(album_model)
		db.session.commit()
		for track in this_album["tracks"]["items"]:
			add_track(track["id"])


def create_sweetmusic_db():
	db.drop_all()
	db.create_all()
	##add_artist("6vwjIs0tbIiseJMR3pqwiL")
	##add_artist("6vwjIs0tbIiseJMR3pqwiL")
	# scrappy()

	# artist_data=get_artist_scrape()
	with open("artists_json.json") as json_file:
		artist_data = json.load(json_file)

	artist_json= artist_data
	create_artist(artist_json)

	# album_data= get_album_scrape()
	with open("albums_json.json") as json_file:
		album_data = json.load(json_file)

	album_json= album_data
	create_album(album_json)

	# tracks_data= get_tracks_scrape()
	with open("tracks_json.json") as json_file:
		track_data = json.load(json_file)

	tracks_json= track_data
	create_tracks(tracks_json)
	create_tracks_album(album_json)