#!flask/bin/python
from models import Artist, Track, Album
import requests
import spotipy
import spotipy.util as util
from db import db 
import json
import os.path
import re
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
		artist_in_track= re.split(',',track['album_name'])
		
		if album == None:
			album_id=None
		else:
			album_id=album.id
		#print(Album.query.all())
			
		tracks_model= tracks_model= Track(track['name'],track['artist_name'],track['release_date'],track['album_name'],track['album']['images'][1]['url'],track['duration_ms'],track['uri'],track['id'],album_id,track['col_img'],track['href'])
		
		for art_tr in artist_in_track:
			
				artist= Artist.query.filter(Artist.name == art_tr).first()
				if(artist== None):
					i=1
				else:	
					tracks_model.artists2.append(artist)
		db.session.add(tracks_model)
		db.session.commit()


def create_sweetmusic_db():
	db.drop_all()
	db.create_all()
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