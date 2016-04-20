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
from helpers import pull_spotify_artists, pull_spotify_tracks, pull_spotify_albums, artist_json, album_json, track_json
import sys
from search_db import search_db

DEFAULT_PAGE_SIZE = 20

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

    # Query database for a specific number of artists and sort and order them if provided arguments
    if 'sort' in request.args:
        if request.args['sort'] == 'artist_name':
            if 'order' in request.args and request.args['order'] == 'desc':
                artists = Artist.query.order_by(Artist.name.desc()).offset(offset).limit(psize).all()
            else:
                artists = Artist.query.order_by(Artist.name).offset(offset).limit(psize).all()
        elif request.args['sort'] == 'num_albums':
            if 'order' in request.args and request.args['order'] == 'desc':
                artists = Artist.query.order_by(Artist.num_albums.desc()).offset(offset).limit(psize).all()
            else:
                artists = Artist.query.order_by(Artist.num_albums).offset(offset).limit(psize).all()
        elif request.args['sort'] == 'recent_album':
            if 'order' in request.args and request.args['order'] == 'desc':
                artists = Artist.query.order_by(Artist.recent_album.desc()).offset(offset).limit(psize).all()
            else:
                artists = Artist.query.order_by(Artist.recent_album).offset(offset).limit(psize).all()
        elif request.args['sort'] == 'top_track':
            if 'order' in request.args and request.args['order'] == 'desc':
                artists = Artist.query.order_by(Artist.top_track.desc()).offset(offset).limit(psize).all()
            else:
                artists = Artist.query.order_by(Artist.top_track).offset(offset).limit(psize).all()
        elif request.args['sort'] == 'popularity':
            if 'order' in request.args and request.args['order'] == 'desc':
                artists = Artist.query.order_by(Artist.popularity.desc()).offset(offset).limit(psize).all()
            else:
                artists = Artist.query.order_by(Artist.popularity).offset(offset).limit(psize).all()
    else:
        artists = Artist.query.offset(offset).limit(psize).all()

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

    # Query database for a specific number of albums and sort if given appropriate arguments
    if 'sort' in request.args:
        if request.args['sort'] == 'album_name':
            if 'order' in request.args and request.args['order'] == 'desc':
                albums = Album.query.order_by(Album.name.desc()).offset(offset).limit(psize).all()
            else:
                albums = Album.query.order_by(Album.name).offset(offset).limit(psize).all()
        elif request.args['sort'] == 'artist_name':
            if 'order' in request.args and request.args['order'] == 'desc':
                albums = Album.query.order_by(Album.artist_name.desc()).offset(offset).limit(psize).all()
            else:
                albums = Album.query.order_by(Album.artist_name).offset(offset).limit(psize).all()
        elif request.args['sort'] == 'release_date':
            if 'order' in request.args and request.args['order'] == 'desc':
                albums = Album.query.order_by(Album.release_date.desc()).offset(offset).limit(psize).all()
            else:
                albums = Album.query.order_by(Album.release_date).offset(offset).limit(psize).all()
        elif request.args['sort'] == 'num_tracks':
            if 'order' in request.args and request.args['order'] == 'desc':
                albums = Album.query.order_by(Album.num_tracks.desc()).offset(offset).limit(psize).all()
            else:
                albums = Album.query.order_by(Album.num_tracks).offset(offset).limit(psize).all()
        elif request.args['sort'] == 'length':
            if 'order' in request.args and request.args['order'] == 'desc':
                albums = Album.query.order_by(Album.length.desc()).offset(offset).limit(psize).all()
            else:
                albums = Album.query.order_by(Album.length).offset(offset).limit(psize).all()
    else:
        albums = Album.query.offset(offset).limit(psize).all()

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
    # Query database for a specific number of tracks and sort and order them if given appropriate arguments
    if 'sort' in request.args:
        if request.args['sort'] == 'track_title':
            if 'order' in request.args and request.args['order'] == 'desc':
                tracks = Track.query.order_by(Track.title.desc()).offset(offset).limit(psize).all()
            else:
                tracks = Track.query.order_by(Track.title).offset(offset).limit(psize).all()
        elif request.args['sort'] == 'artist_name':
            if 'order' in request.args and request.args['order'] == 'desc':
                tracks = Track.query.order_by(Track.artist_name.desc()).offset(offset).limit(psize).all()
            else:
                tracks = Track.query.order_by(Track.artist_name).offset(offset).limit(psize).all()
        elif request.args['sort'] == 'release_date':
            if 'order' in request.args and request.args['order'] == 'desc':
                tracks = Track.query.order_by(Track.release_date.desc()).offset(offset).limit(psize).all()
            else:
                tracks = Track.query.order_by(Track.release_date).offset(offset).limit(psize).all()
        elif request.args['sort'] == 'album_name':
            if 'order' in request.args and request.args['order'] == 'desc':
                tracks = Track.query.order_by(Track.album_name.desc()).offset(offset).limit(psize).all()
            else:
                tracks = Track.query.order_by(Track.album_name).offset(offset).limit(psize).all()
        elif request.args['sort'] == 'duration':
            if 'order' in request.args and request.args['order'] == 'desc':
                tracks = Track.query.order_by(Track.duration.desc()).offset(offset).limit(psize).all()
            else:
                tracks = Track.query.order_by(Track.duration).offset(offset).limit(psize).all()
    else:
        tracks = Track.query.offset(offset).limit(psize).all()
    
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

        json = {'tracks': []}

        ids_not_in_db = []
        for i in ids:
            tracks = Track.query.filter(Track.spotify_id.like(i)).all()

            if len(tracks) > 0:
                for track in tracks:
                    json['tracks'].append(track_json(track))

            else:
                ids_not_in_db.append(i)
        # Now that we have gone through each id looking through out database, let's search spotify for ids that had no match
        if len(ids_not_in_db) > 0:
            spotify_tracks = pull_spotify_tracks(ids_not_in_db)
            # append found tracks to returning data
            for spot_track in spotify_tracks:
                json['tracks'].append(track_json(spot_track))
            # json['tracks'].append(spotify_tracks['tracks'])

        return jsonify(json)
    # Get arbitrary tracks if none specified
    else:
        return jsonify({"tracks": []})

# ------
# Search
# ------

# Simple implementation
@app.route('/search/<table>')
def search(table):
    req = {}

    req['table'] = table
    if table != 'artists' and table != 'albums' and table != 'tracks':
        req['table'] = 'all'

    req['searchterm'] = request.args['searchterm']
    results = search_db(request.args['searchterm'])

    return jsonify(results)

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
    output = subprocess.getoutput("python tests.py")
    return json.dumps({'output': str(output)})


# -------------
# ILDB API call
# -------------

@app.route('/get_legislators')
def get_legislators():
    legislators = requests.get('http://ildb.me/api/legislators')
    return json.dumps({'legislators': legislators.json()})


# ---------------
# Main page route
# ---------------

@app.route('/')
def splash():
    return send_file('index.html')


if __name__ == "__main__":
    manager.run()
