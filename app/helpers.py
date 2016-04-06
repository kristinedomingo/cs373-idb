from flask import Flask, render_template, send_file
from flask import jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
from db import db, app , manager
from models import Artist, Album, Track, artists, artists2
import json
import requests
from datetime import timedelta

# ----------------
# HELPER FUNCTIONS
# ----------------

def pull_spotify_artists(spotify_ids):
        
    # artist = requests.get(
    #     'https://api.spotify.com/v1/artists/?ids=' + spotify_id).json()
    return None

def pull_spotify_albums(spotify_ids):
    return None

def pull_spotify_tracks(spotify_ids):
    # List of track dicts that will be returned
    tracks = []

    # combine ids into string for spotify request
    ids = ""
    for i in spotify_ids:
        ids += i + ', '
    ids = ids.rstrip(', ')

    # Contact spotify will all unstored ids and return 
    spot_tracks = requests.get(
            'https://api.spotify.com/v1/tracks?ids=' + ids).json()
    
    print (spot_tracks, file=sys.stderr)

    # go through returned tracks from spotify and make database objects for them
    for t in spot_tracks['tracks']:
        # if t != null
        album_id = None
        release_date = None
        album = Album.query.filter(Album.name == t['album']['name']).first()
        artists_in_track = []
        for artist in t['artists']:
            artists_in_track.append(artist['name'])

        # combine artist names into a comma separated list
        artist_names = ""
        for i in t['artists']:
            artist_names += i['name'] + ', '
        artist_names = artist_names.rstrip(', ')

        if album == None:
            album_id = None
        else:
            album_id = album.id
            release_date = album.release_date

        track = Track(t['name'], artist_names, release_date, t['album']['name'], t['album']['images'][1]['url'], t['duration_ms'], t['uri'], t['id'], album_id, t['album']['images'][2]['url'], t['href'])


        for art_tr in artists_in_track:
            artist = Artist.query.filter(Artist.name == art_tr).first()
            if artist == None:
                i = 1
            else:
                track.artists2.append(artist)
        db.session.add(track)
        db.session.commit()

        # Add track json to list
        tracks.append(track)
    return tracks

def artist_json(artist):
    artist_json = {
        'id': artist.spotify_id,
        'name': artist.name,
        'num_albums': artist.num_albums,
        'recent_album': artist.recent_album,
        'top_track': artist.top_track,
        'popularity': artist.popularity,
        'spotify_uri': artist.spotify_uri,
        'db_id': artist.id,
        'col_img': {'url': artist.col_img}
    }

    return artist_json

def album_json(album):
    album_artists = []
    for artist in album.artists:
        album_artists.append(artist_json(artist))

    album_tracks = []
    for track in album.tracks:
        album_tracks.append(track_json(track))

    album_json = {
        'id': album.spotify_id,
        'name': album.name,
        'release_date': album.release_date,
        'length': album.length,
        # 'col_img': album.col_img,
        'num_tracks': album.num_tracks,
        'spotify_uri': album.spotify_uri,
        # 'spotify_id': album.spotify_id,
        'images': album.images,
        # 'href': album.href,
        'artist_name': album.artist_name,
        'col_img': {'url': album.col_img},
        'artists': album_artists,
        'tracks': album_tracks,
        'db_id': album.id
    }

    return album_json

def track_json(track):
    duration = timedelta(milliseconds = track.duration)
    minutes = str(duration.seconds // 60)
    seconds = str(duration.seconds % 60).zfill(2)

    artists_array = []
    for artist in track.artists2:
        artists_array.append({'artist_name': artist.name, 'artist_id': artist.spotify_id})

    track_json = {
        'id': track.spotify_id,
        'name': track.title,
        'release_date': track.release_date,
        'spotify_uri': track.spotify_uri,
        'duration_ms': track.duration,
        'spotify_id': track.spotify_id,
        'duration': minutes + ':' + seconds,         #duplicate?
        # 'artists': track.artists,
        'album': track.album,
        'album_cover_url': track.album_cover_url,
        # 'col_img': track.col_img,
        # 'href': track\.spotify_uri,        #different from uri?
        'album_name': track.album,
        'artist_name': track.artist_name,
        'db_id': track.id,
        'col_img': {'url': track.col_img},
        'artists': artists_array
    }

    return track_json

# --------------------------------------