from flask import Flask, render_template, send_file
from flask import jsonify
import requests

app = Flask(__name__, static_url_path='')

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
        top_track = requests.get(
            'https://api.spotify.com/v1/artists/' + artist["id"] + '/top-tracks?country=US').json()["tracks"][0]
        # add a new K/V pair to artist dict
        artist["top_track"] = top_track["name"]

        # Request returns {"items" : [{...}]}
        # https://developer.spotify.com/web-api/get-artists-albums/
        albums = requests.get(
            'https://api.spotify.com/v1/artists/' + artist["id"] + '/albums').json()["items"]
        # Assumming that spotify gives us the list of albums in reverse
        # chronological order
        last_album = albums[0]["name"]
        artist["last_album"] = last_album
        artist["num_albums"] = len(albums)
        artist["col_img"] = artist["images"][len(artist["images"]) - 1]["url"]

    return jsonify(artists)


@app.route('/')
def splash():
    return send_file('index.html')


@app.route('/get_albums')
def album_ajax():
    albums = requests.get(
        'https://api.spotify.com/v1/albums/?ids=6bfkwBrGYKJFk6Z4QVyjxd,28AwWnNskZq7zvJs5oEHGc,1zW59tdlltJgHOlqLbR1lN')
    return jsonify(albums.json())


@app.route('/get_tracks')
def track_ajax():
    tracks = requests.get(
        'https://api.spotify.com/v1/tracks/?ids=0LSl4lXvjrdGORyBGB2lNJ,6ZpR2XFuQJSHAQwg9495KZ,4URU1lRXhWwZIXuxKI1SuH')
    return jsonify(tracks.json())

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
