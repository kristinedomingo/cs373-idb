from sqlalchemy import *

from db import db
#The data table for the many to many relationships we have#
#Many to many relationships artists and tracks.
#many to many relationships between artist and album 
artists = db.Table('artists',
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')),
    db.Column('album_id', db.Integer, db.ForeignKey('album.id')))

artists2= db.Table('artists2',
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')),
    db.Column('track_id', db.Integer, db.ForeignKey('track.id')))

"""
Albums:
   - name
   - release_date
   - length
   - col_img
   - num_tracks
   - uri
   - id
   - images
"""
class Album(db.Model) :
    """
    Album Model
    Has an id, name, date, length, number of tracks, artist
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    artist_name = db.Column(db.String(80))
    release_date = db.Column(db.String(80))
    length = db.Column(db.String(100))
    num_tracks = db.Column(db.Integer)
    spotify_uri= db.Column(String(100))
    spotify_id = db.Column(String(100))
    images = db.Column(String(250))
    col_img = db.Column(String(250))
    href=db.Column(String(250))

    #This is the many to many relationship between artist and album connect to the table
    artists = db.relationship('Artist', secondary=artists,
        backref=db.backref('albums', lazy='dynamic'))

    #This is the one to many relationship for album and track.
    tracks= db.relationship('Track',backref='my_album', lazy='dynamic')
    

    def __init__(self, name, artist_name , release_date, length, num_tracks, spotify_uri, spotify_id, images, col_img,href):
        self.name = name
        self.artist_name= artist_name
        self.release_date = release_date
        self.length= length
        self.num_tracks= num_tracks
        self.spotify_uri= spotify_uri
        self.spotify_id= spotify_id
        self.images= images
        self.col_img=col_img
        self.href= href


    def __repr__(self):
        return '<User %r>' % self.name
"""
Artist:
   - id
   - popularity (int)
   - col_img
   - name
   - uri
   - last_album
   - num_albums
   - images
   - followers (int)
   - top_track
"""
class Artist(db.Model) :
    """
    Artist Model
    Has id, name, num_albums, recent albums, top track, popularity, Spotify uri, Spotify id
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    num_albums = db.Column(db.Integer)
    recent_album= db.Column(db.String(100))
    top_track = db.Column(db.String(100))
    popularity = db.Column(db.Integer)
    spotify_uri= db.Column(String(100))
    spotify_id = db.Column(String(100))
    images = db.Column(String(250))
    col_img =db.Column(String(250))
    followers = db.Column(Integer)
    
    def __init__(self, name, num_albums, recent_album, top_track, popularity, spotify_uri, spotify_id,images, col_img, followers):
        self.name = name
        self.num_albums = num_albums
        self.recent_album= recent_album
        self.top_track = top_track
        self.popularity = popularity
        self.spotify_uri= spotify_uri
        self.spotify_id= spotify_id
        self.images=images
        self.col_img= col_img
        self.followers= followers

    def __repr__(self):
        return '<User %r>' % self.name
"""
Tracks:
   - name
   - release_date
   - uri
   - duration_ms
   - id
   - duration
   - artists
   - album
   - col_img
   - href
   - album_name
   - artist_name
"""

class Track(db.Model) :
    """
    Track Model
    Has id, name, artist name, release, album, duration, and etc.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    artist_name= db.Column(db.String(100))
    release_date = db.Column(db.String(100))
    album = db.Column(db.String(100))
    album_cover_url = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    spotify_uri= db.Column(String(100))
    spotify_id = db.Column(String(100))
    col_img = db.Column(String(250))
    href = db.Column(String(250))


    # This is the link between the table that connects many to many relationships.
    artists2 = db.relationship('Artist', secondary=artists2,
        backref=db.backref('tracks', lazy='dynamic'))
    #This is what connects the one to many relationship between tracks and album id.
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))

    def __init__(self, title, artist_name, release, album, album_cover_url, duration, spotify_uri, spotify_id, album_id, col_img, href):
        id = db.Column(db.Integer, primary_key=True)
        self.title = title
        self.artist_name= artist_name
        self.release_date = release
        self.album = album
        self.album_cover_url = album_cover_url
        self.duration = duration
        self.spotify_uri= spotify_uri
        self.spotify_id= spotify_id
        self.album_id=album_id
        self.col_img=col_img
        self.href=href
    def __repr__(self):
        return '<User %r>' % self.title