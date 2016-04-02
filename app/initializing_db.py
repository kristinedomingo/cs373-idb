#!flask/bin/python
from models import Artist, Track, Album
import requests
import spotipy
import spotipy.util as util
from db import db 
import json
import os.path
from scraper import scrappy, get_artist_scrape, get_album_scrape, get_tracks_scrape


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
		album_model= Album(album['name'],album['artist_name'], album['release_date'],album['length'],album['num_tracks'],album['uri'],album['id'],album['images'][1]['url'],album['col_img'])
		db.session.add(album_model)
		db.session.commit()
def create_tracks(track_json):
	
	for track in track_json['tracks']:
		#print(track['name'])

		album= Album.query.filter(Album.name ==track['album_name']).first()
		print(Album.query.all())
		tracks_model= Track(track['name'],track['artist_name'],track['release_date'],track['album_name'],track['duration_ms'],track['uri'],track['id'],1,track['col_img'],track['href'])
		db.session.add(tracks_model)
		db.session.commit()

def create_sweetmusic_db():
	db.drop_all()
	db.create_all()
	scrappy()
	artist_data=get_artist_scrape()
	"""
	scriptpath = os.path.dirname(__file__)
	filename = os.path.join(scriptpath, 'artists_json.json')
	artist_data= open(filename)
	"""
	artist_json= artist_data
	create_artist(artist_json)
	album_data= get_album_scrape()
	"""
	scriptpath = os.path.dirname(__file__)
	filename = os.path.join(scriptpath, 'albums_json.json')
	album_data= open(filename)
	"""
	album_json= album_data
	create_album(album_json)
	"""
	scriptpath = os.path.dirname(__file__)
	filename = os.path.join(scriptpath, 'tracks_json.json')
	tracks_data= open(filename)
	"""
	tracks_data= get_tracks_scrape()
	tracks_json= tracks_data
	create_tracks(tracks_json)