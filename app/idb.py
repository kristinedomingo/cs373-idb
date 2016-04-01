from flask import Flask, render_template, send_file
from flask import jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
from db import db, app , manager
import subprocess
import requests
import json
from datetime import timedelta
from initializing_db import create_sweetmusic_db
from models import Artist, Album, Track
import sys

DEFAULT_PAGE_SIZE = 10

# ---------------
# get_artist_data
# ---------------

@app.route('/get_artists')
def get_artist_data():
    """
    Calls the spotify three times for different sets of data to be passed to the front end
    templating system.

    returns a response/json objects 
    More info on Spotify Artist Objects here : https://developer.spotify.com/web-api/object-model/#artist-object-full
    """

    # returns json in the form {"artists": [artistobj1,...artistobjN]}
    artists = requests.get(
        'https://api.spotify.com/v1/artists?ids=2Q0MyH5YMI5HPQjFjlq5g3,6107PIkQDuEUcdpZqSzQsu,1HxJeLhIuegM3KgvPn8sTa').json()

    # run through each artist and append items to the respective artists in
    # the artist obj
    for artist in artists["artists"]:

        # Request returns json in the form {"tracks":[{...}]}
        # https://developer.spotify.com/web-api/get-artists-top-tracks/
        top_track = requests.get(artist["href"] + '/top-tracks?country=US').json()["tracks"][0]

        # add a new K/V pair to artist dict
        artist["top_track"] = {"name" : top_track["name"], "id" : top_track["id"]}

        # Request returns {"items" : [{...}]}
        # https://developer.spotify.com/web-api/get-artists-albums/
        albums = requests.get(artist["href"] + '/albums').json()["items"]

        # Assumming that spotify gives us the list of albums in reverse
        # chronological order
        last_album = albums[0]["name"]
        artist["last_album"] = {"name":last_album, "id": albums[0]["id"]}
        artist["num_albums"] = len(albums)
        artist["col_img"] = artist["images"][len(artist["images"]) - 1]["url"]

    return jsonify(artists)


# --------------
# get_album_data
# --------------

@app.route('/get_albums')
def get_album_data():
    #11wzEOXFI1wgBHxKcsbacJ Chet Faker 1998 Melbourne Edition 
    #3vNsiDEAnZRleKelEgdet1 Atlast Bound Lullaby 
    #6bfkwBrGYKJFk6Z4QVyjxd Jack U Skrillex and Diplo present Jack \u00dc
    albums = requests.get(
        'https://api.spotify.com/v1/albums/?ids=11wzEOXFI1wgBHxKcsbacJ,3vNsiDEAnZRleKelEgdet1,6bfkwBrGYKJFk6Z4QVyjxd').json()

    # Parse JSON information to append needed items
    for album in albums["albums"]:

        # Get album cover
        album["col_img"] = album["images"][len(album["images"]) - 1]["url"]

        # Get artist(s)
        names = ""
        for artist in album["artists"]:
            names += artist["name"] + ', '
        album["artist_name"] = names.rstrip(', ')

        # Get number of tracks
        album["num_tracks"] = len(album["tracks"]["items"])

        # Get length (duration) of album
        duration_ms = 0
        for track in album["tracks"]["items"]:
            duration_ms += track["duration_ms"]
        duration = timedelta(milliseconds = duration_ms)

        # Convert milliseconds to a human-readable time
        minutes = str(duration.seconds // 60)
        seconds = str(duration.seconds % 60).zfill(2)
        album["length"] = minutes + ":" + seconds

    return jsonify(albums)


# --------------
# get_track_data
# --------------

@app.route('/get_tracks')
def get_track_data():

    #4KtrE35pTuqwNc22QP58RT Drop the Game Chet Faker
    #6SXRLE3kFht3wi0glxDueW Landed on Mars Atlas Bound
    #66hayvUbTotekKU3H4ta1f Where Are \u00dc Now (with Justin Bieber) Jack U
    tracks = requests.get(
        'https://api.spotify.com/v1/tracks/?ids=4KtrE35pTuqwNc22QP58RT,6SXRLE3kFht3wi0glxDueW,66hayvUbTotekKU3H4ta1f').json()

    # Parse JSON information to append needed items
    for track in tracks["tracks"]:

        # Get track album cover
        track["col_img"] = track["album"]["images"][len(track["album"]["images"]) - 1]["url"]

        # Get artist(s)
        names = ""
        for artist in track["artists"]:
            names += artist["name"] + ', '
        track["artist_name"] = names.rstrip(', ')

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

    return jsonify(tracks)


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

    # Query database for a specific number of artists
    artists = Artist.query.limit(psize).all()
    i = 0

    # From the returned artists format the data for the front-end
    for artist in artists:
        json['artists'].append({
                'id': artist.spotify_id,
                'name': artist.name,
                'num_albums': artist.num_albums,
                'recent_album': artist.recent_album,
                'top_track': artist.top_track,
                'popularity': artist.popularity,
                'spotify_uri': artist.spotify_uri,
                'db_id': artist.id
            })
        i += 1

    return jsonify(json)

@app.route('/artists')
def artists():
    # Get specified artists by their ids
    if 'ids' in request.args:
        ids = request.args.get('ids').split(',')
        return jsonify({"ids": ids})
        
        # Query the database for artists that match the list of ids provided
        # artists_q = Artist.query.filter(_or(*[Artist.spotify_id.like(i) for i in request.args['ids']]))
        # json = {'artists': []}

        # # From the returned artists format the data for the front-end
        # for artist in artists_q:
        #     artist_q.query.like()
        #     json['artists'].append({
        #             'id': artist.spotify_id,
        #             'name': artist.name,
        #             'num_albums': artist.num_albums,
        #             'recent_album': artist.recent_album,
        #             'top_track': artist.top_track,
        #             'popularity': artist.popularity,
        #             'spotify_uri': artist.spotify_uri,
        #             'db_id': artist.id
        #         })
        # return jsonify(json)

    
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

    # Query database for a specific number of albums
    albums = Album.query.limit(psize).all()
    i = 0

    # From the returned albums format the data for the front-end
    for album in albums:
        # Convert milliseconds to a human-readable time
        duration = timedelta(milliseconds = album.length)
        minutes = str(duration.seconds // 60)
        seconds = str(duration.seconds % 60).zfill(2)

        json['albums'].append({
                'id': album.spotify_id,
                'name': album.name,
                # 'release_date': album.release_date,
                'length': minutes + ':' + seconds,
                # 'col_img': album.col_img,
                'num_tracks': album.num_tracks,
                'spotify_uri': album.spotify_uri,
                # 'spotify_id': album.spotify_id,
                # 'images': album.images,
                # 'href': album.href,
                'artist_name': album.artist_name#,
                # 'artists': album.artists,
                # 'tracks': album.tracks
            })
        i += 1

    return jsonify(json)

@app.route('/albums')
def albums():
    # Get specified albums by their ids
    if 'ids' in request.args:
        ids = request.args.get('ids').split(',')
        return jsonify({"ids": ids})
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

    i = 0
    # Query database for a specific number of tracks
    tracks = Track.query.limit(psize).all()
    
    # From the returned tracks format the data for the front-end
    for track in tracks:
        duration = timedelta(milliseconds = track.duration)
        minutes = str(duration.seconds // 60)
        seconds = str(duration.seconds % 60).zfill(2)

        json['tracks'].append({
                'id': track.spotify_id,
                'name': track.title,
                'release_date': track.release_date,
                'spotify_uri': track.spotify_uri,
                'duration_ms': track.duration,
                'spotify_id': track.spotify_id,
                'duration': minutes + ':' + seconds,         #duplicate?
                # 'artists': track.artists,
                'album': track.album,
                # 'col_img': track.col_img,
                # 'href': track\.spotify_uri,        #different from uri?
                'album_name': track.album,
                'artist_name': track.artist_name,
                'db_id': track.id
            })
        i += 1

    return jsonify(json)

@app.route('/tracks')
def tracks():
    # Get specified tracks by their ids
    if 'ids' in request.args:
        ids = request.args.get('ids').split(',')
        return jsonify({"ids": ids})
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
    logger.debug("drop_db")
    app.config['SQLALCHEMY_ECHO'] = True
    db.drop_all()


# ---------
# run_tests
# ---------

@app.route('/run_tests')
def run_tests():
    output = subprocess.getoutput("make test")
    return json.dumps({'output': str(output)})


@app.route('/')
def splash():
    return send_file('index.html')


if __name__ == "__main__":
    manager.run()
    #Commenting out this for now based on what
    # was in the Carina tutorial
    # app.run(host='0.0.0.0', debug=True)
