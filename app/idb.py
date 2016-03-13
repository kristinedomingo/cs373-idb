from flask import Flask, render_template
from flask import jsonify
import requests

app = Flask(__name__, static_url_path='')


@app.route('/')
def splash():
    return app.send_static_file('index.html')

@app.route('/artists')
def artists():
    return render_template('artists.html')

@app.route('/get_artists')
def artist_ajax():
    # This request requires a comma separated list of artist IDs which can be
    # found via the Spotify URI accessed through the app or web
    artists = requests.get(
        'https://api.spotify.com/v1/artists?ids=2Q0MyH5YMI5HPQjFjlq5g3,6107PIkQDuEUcdpZqSzQsu,1HxJeLhIuegM3KgvPn8sTa')
    return jsonify(artists.json())


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

@app.route('/about')
def about():
    return app.send_static_file('about.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
