from flask import Flask, render_template, send_file
from flask import jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
from db import db, app , manager
import subprocess
import requests
import json
from datetime import timedelta
from initializing_db import create_sweetmusic_db
from models import Artist, Album, Track, artists, artists2
import sys

DEFAULT_PAGE_SIZE = 10

# ---------------
# get_artist_data
# ---------------

@app.route('/get_artists/<int:page>')
def get_artist_data(page):
    """
    Calls the spotify three times for different sets of data to be passed to the front end
    templating system.

    returns a response/json objects 
    More info on Spotify Artist Objects here : https://developer.spotify.com/web-api/object-model/#artist-object-full
    """

    return artist_table(page)


# --------------
# get_album_data
# --------------

@app.route('/get_albums/<int:page>')
def get_album_data(page):
    return album_table(page)


# --------------
# get_track_data
# --------------

@app.route('/get_tracks/<int:page>')
def get_track_data(page):
    return track_table(page)


# -----------------
# Mock up API stubs
# -----------------

# This references data base e
@app.route('/artists/<int:page>')
def artist_table(page):
    json = {'page': page}
    json['artists'] = []

    psize = DEFAULT_PAGE_SIZE
    if 'psize' in request.args:
        psize = int(request.args['psize'])
        json['psize'] = psize

    offset = (page - 1) * psize
    # Query database for total artists
    artists_count = Artist.query.count()
    json['total_artists'] = artists_count
    # Query database for a specific number of artists
    artists = Artist.query.offset(offset).limit(psize).all()
    # artists = Artist.query.limit(psize).all()
    i = 0

    # From the returned artists format the data for the front-end
    for artist in artists:
        json['artists'].append(artist_json(artist))
        i += 1

    return jsonify(json)

@app.route('/artists')
def artists_route():
    # Get specified artists by their ids
    if 'ids' in request.args:
        ids = request.args.get('ids').split(',')
        
        # Query the database for artists that match the list of ids provided
        json = {'artists': []}

        ids_not_in_db = []
        # From the returned artists format the data for the front-end
        for i in ids:
            # json['artists'].append({'id': i})
            artists = Artist.query.filter(Artist.spotify_id.like(i)).all()
            
            print (artists, file=sys.stderr)
            # Should only return one artist per id but just in case
            if len(artists) > 0:
                for artist in artists:
                    json['artists'].append(artist_json(artist))
            else:
                ids_not_in_db.append(i)
        # Now that we have gone through each id looking through out database, let's search spotify for ids that had no match
        if len(ids_not_in_db) > 0:
            spotify_data = pull_spotify_artists(ids_not_in_db)

        return jsonify(json)

    
    # Get arbitrary artists
    else:
        return jsonify({"artists": []})


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
    return None

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

@app.route('/albums/<int:page>')
def album_table(page):
    json = {'page': page}
    json['albums'] = []

    psize = DEFAULT_PAGE_SIZE
    if 'psize' in request.args:
        psize = int(request.args['psize'])
        json['psize'] = psize

    offset = (page - 1) * psize
    # Query for total number of albums in database
    album_count = Album.query.count()
    json['total_albums'] = album_count
    # Query database for a specific number of albums
    albums = Album.query.offset(offset).limit(psize).all()
    # albums = Album.query.limit(psize).all()
    i = 0

    # From the returned albums format the data for the front-end
    for album in albums:
        json['albums'].append(album_json(album))
        i += 1

    return jsonify(json)

@app.route('/albums')
def albums_route():
    # Get specified albums by their ids
    if 'ids' in request.args:
        ids = request.args.get('ids').split(',')
        albums = Album.query.filter(Album.spotify_id.in_(ids))

        json = {"ids": ids}
        json['albums'] = []

        for album in albums:
            json['albums'].append(album_json(album))

        return jsonify(json)
    # Get arbitrary albums if none specified
    else:
        return jsonify({"albums": []})

@app.route('/tracks/<int:page>')
def track_table(page):
    json = {'page': page}
    json['tracks'] = []

    psize = DEFAULT_PAGE_SIZE
    if 'psize' in request.args:
        psize = int(request.args['psize'])
        json['psize'] = psize

    offset = (page - 1) * psize
    i = 0
    # Query database for total tracks
    track_count = Track.query.count()
    json['total_count'] = track_count
    # Query database for a specific number of tracks
    tracks = Track.query.offset(offset).limit(psize).all()
    # tracks = Track.query.limit(psize).all()
    
    # From the returned tracks format the data for the front-end
    for track in tracks:
        json['tracks'].append(track_json(track))
        i += 1

    return jsonify(json)

@app.route('/tracks')
def tracks_route():
    # Get specified tracks by their ids
    if 'ids' in request.args:
        ids = request.args.get('ids').split(',')
        tracks = Track.query.filter(Track.spotify_id.in_(ids))

        json = {"ids": ids}
        json['tracks'] = []

        for track in tracks:
            json['tracks'].append(track_json(track))

        return jsonify(json)
    # Get arbitrary tracks if none specified
    else:
        return jsonify({"tracks": []})

@manager.command
def create_db():
    #logger.debug("create_db")
    app.config['SQLALCHEMY_ECHO'] = True
    create_sweetmusic_db()

@manager.command
def drop_db():
    # logger.debug("drop_db")
    app.config['SQLALCHEMY_ECHO'] = True
    db.drop_all()


# ---------
# run_tests
# ---------

@app.route('/run_tests')
def run_tests():
    output = subprocess.getoutput("python3 tests.py")
    return json.dumps({'output': str(output)})


@app.route('/')
def splash():
    return send_file('index.html')


if __name__ == "__main__":
    manager.run()
    #Commenting out this for now based on what
    # was in the Carina tutorial
    # app.run(host='0.0.0.0', debug=True)
