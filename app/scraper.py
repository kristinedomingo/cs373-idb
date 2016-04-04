import requests
import json
from collections import deque
from datetime import timedelta

artists_json = {"artists" : []}
albums_json = {"albums" : []}
tracks_json = {"tracks" : []}

artists_queue = deque()
albums_queue = deque()
tracks_queue = deque()

scraped_artists = []
scraped_albums = []
scraped_tracks = []

ARTIST_IDS = ["26T3LtbuGT1Fu9m0eRq5X3", # Cage the Elephant
              "4dpARuHxo51G3z768sgnrY", # Adele
              "25u4wHJWxCA9vO0CzxAbK7", # Lukas Graham
              "5ZsFI1h6hIdQRw2ti0hz81", # ZAYN
              "3YQKmKGau1PzlVlkL1iodx", # Twenty One Pilots
              "5WUlDfRSoLAfcVSX1WnrxN", # Sia
              "69GGBxA162lTqCwzJG5jLp", # The Chainsmokers
              "66CXWjxzNUsdJxJ2JdwvnR", # Ariana Grande
              "1uNFoZAHBGtllmzznpCI3s"] # Justin Bieber

def scrape(ids):
    global artists_queue
    global albums_queue
    global tracks_queue

    # Add artists to queue to kick off scraping
    for artist_id in ids:
        artists_queue.append(artist_id)
        scraped_artists.append(artist_id)

    while artists_queue or albums_queue or tracks_queue:
        scrape_artist()
        scrape_tracks()
        scrape_albums()

def scrape_artist():
    global artists_json
    global artists_queue
    global albums_queue
    global tracks_queue
    global scraped_tracks
    global scraped_albums

    while artists_queue:
        print("Scraping an artist...")
        # Get the json
        this_artist = requests.get('https://api.spotify.com/v1/artists/' + artists_queue.popleft()).json()

        # Get and add the top track, and add track to queue
        top_tracks = requests.get(this_artist["href"] + '/top-tracks?country=US').json()["tracks"]
        if top_tracks:
            this_artist["top_track"] = {"name" : top_tracks[0]["name"], "id" : top_tracks[0]["id"]}
            if top_tracks[0]["id"] not in scraped_tracks and len(scraped_tracks) < 350:
                scraped_tracks.append(top_tracks[0]["id"])
                tracks_queue.append(top_tracks[0]["id"])

        # Get and add most recent album, and add album to queue
        albums = requests.get(this_artist["href"] + '/albums').json()["items"]
        last_album = albums[0]["name"]
        this_artist["last_album"] = {"name":last_album, "id": albums[0]["id"]}
        if albums[0]["id"] not in scraped_albums and len(scraped_albums) < 250:
            scraped_albums.append(albums[0]["id"])
            albums_queue.append(albums[0]["id"])

        # Add extra information (number of albums, album cover)
        this_artist["num_albums"] = len(albums)
        if this_artist["images"]:
            this_artist["col_img"] = this_artist["images"][len(this_artist["images"]) - 1]["url"]

        # Delete information that is not going to be used
        not_needed = ["genres", "external_urls"]
        for element in not_needed:
            del this_artist[element]
            
        # Add completed artist information to json
        artists_json["artists"].append(this_artist)

def scrape_tracks():
    global tracks_queue
    global artists_queue
    global tracks_json
    global scraped_artists

    while tracks_queue:
        print("Scraping a track...")
        # Get the track json
        this_track = requests.get('https://api.spotify.com/v1/tracks/' + tracks_queue.popleft()).json()

        # Get track album cover
        if this_track["album"]["images"]:
            this_track["col_img"] = this_track["album"]["images"][len(this_track["album"]["images"]) - 1]["url"]

        # Get artist(s), and add to artist queue
        names = ""
        for artist in this_track["artists"]:
            names += artist["name"] + ', '
            if artist["id"] not in scraped_artists and len(scraped_artists) < 200:
                scraped_artists.append(artist["id"])
                artists_queue.append(artist["id"])
        this_track["artist_name"] = names.rstrip(', ')

        # Get associated album
        this_track["album_name"] = this_track["album"]["name"]

        # Get release date from album
        album_href = this_track["album"]["href"]
        album_json = requests.get(album_href).json()
        this_track["release_date"] = album_json["release_date"]

        # Get track duration
        duration = timedelta(milliseconds = this_track["duration_ms"])
        minutes = str(duration.seconds // 60)
        seconds = str(duration.seconds % 60).zfill(2)
        this_track["duration"] = minutes + ":" + seconds

        # Delete information that is not going to be used
        not_needed = ["external_urls", "preview_url", "external_ids"]
        for element in not_needed:
            del this_track[element]

        # Add completed track information to json
        tracks_json["tracks"].append(this_track)

def scrape_albums():
    global albums_json
    global albums_queue
    global tracks_queue
    global artists_queue
    global scraped_artists
    global scraped_tracks

    while albums_queue:
        print("Scraping an album...")
        # Get the track json
        this_album = requests.get('https://api.spotify.com/v1/albums/' + albums_queue.popleft()).json()

        # Get album cover
        this_album["col_img"] = this_album["images"][len(this_album["images"]) - 1]["url"]

        # Get artist(s), and add to artists queue
        names = ""
        for artist in this_album["artists"]:
            names += artist["name"] + ', '
            if artist["id"] not in scraped_artists and len(scraped_artists) < 200:
                scraped_artists.append(artist["id"])
                artists_queue.append(artist["id"])
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
        for track in this_album["tracks"]["items"]:
            if track["id"] not in scraped_tracks and len(scraped_tracks) < 350:
                scraped_tracks.append(track["id"])
                tracks_queue.append(track["id"])

        # Add completed album information to json
        albums_json["albums"].append(this_album)


# Perform the scraping
def scrappy():
    scrape(ARTIST_IDS)
def get_artist_scrape():
    return artists_json
def get_album_scrape():
    return albums_json
def get_tracks_scrape():
    return tracks_json


# Write to files

scrappy()
artist_file = open('artists_json.json', 'w+')
artist_file.write(json.dumps(artists_json, indent = 2))

album_file = open('albums_json.json', 'w+')
album_file.write(json.dumps(albums_json, indent = 2))

track_file = open('tracks_json.json', 'w+')
track_file.write(json.dumps(tracks_json, indent = 2))

# Print information about what was scraped
print(str(len(artists_json["artists"])) + " artists scraped")
print(str(len(tracks_json["tracks"])) + " tracks scraped")
print(str(len(albums_json["albums"])) + " albums scraped")
