import unittest
from flask.ext.testing import TestCase
from app.db import db, app
from models import Album, Artist, Track
class TestArtist(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
        return app

    def setUp(self):
        db.create_all()
        artist = Artist("Atlas Bound", 8, "Lullaby", "Landed on Mars", 42, "alsjdflkasjd", "http")
        artist2 = Artist("Chet Faker", 20, "1998 Melbourne Edition", "Drop the Game",76, "asffagd", "http")
        db.session.add(artist)
        db.session.add(artist2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Tests that the total # of artists is equal to 2 (created at SetUp)
    def test_get_all_artist(self):
        artists = Artist.query.all()
        assert len(artists) == 2

    # Tests simple selections from the table match expected values
    def test_filtering_artist(self):   
        artist = Artist.query.filter(Artist.recent_album == 'Lullaby').first()
        assert artist.name == "Atlas Bound" and artist.popularity  == 42

        artist = Artist.query.filter(Artist.popularity > 47).first()
        assert artist.name == 'Chet Faker' and artist.recent_album == '1998 Melbourne Edition'

    # Tests adding a new artist and removing that artist from the db
    def test_add_delete_artist(self):
        artists = Artist("Jack U", 14, "Skrillex and Diplo present Jack U", "Where Are U Now ( with Justin Bieber )", 42, "asldfjalieiuyhak", "http")
        db.session.add(artists)
        db.session.commit()
        assert len(Artist.query.all()) == 3

        Artist.query.filter(Artist.name == 'Jack U').delete()
        db.session.commit()
        assert len(Artist.query.all()) == 2

class TestAlbum(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
        return app

    def setUp(self):
        db.create_all()
        album = Album("1998 Melbourne Edition", "Chet Faker", "2015-05-18", 1923800, 5, "asdfasdf", "http")
        album2 = Album("Lullaby", "Atlas Bound", "2016-03-18", 220000, 1, "oiuohkjt", "http")
        db.session.add(album)
        db.session.add(album2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Tests that the total # of albums is equal to 2 (created at SetUp)
    def test_get_all_albums(self):
        album = Album.query.all()
        assert len(album) == 2

    # Tests simple selections from the db match expected values
    def test_filtering_album(self):   
        album = Album.query.filter(Album.name == 'Lullaby').first()
        assert album.artist_name == "Atlas Bound" and album.num_tracks  == 1

        album = Album.query.filter(Album.num_tracks > 2).first()
        assert album.artist_name == 'Chet Faker' and album.name == '1998 Melbourne Edition'

    # Tests adding a new album to the table and removing it
    def test_add_delete_album(self):
        album = Album( "Skrillex and Diplo present Jack U", "Jack U, Skrillex, Diplo", "2015-02-24", 2125000, 10, "abnoioighkjkcjkh", "http")
        db.session.add(album)
        db.session.commit()
        assert len(Album.query.all()) == 3

        Album.query.filter(Album.length >= 2125000).delete()
        db.session.commit()
        assert len(Album.query.all()) == 2


class TestTrack(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
        return app

    def setUp(self):
        db.create_all()
        track = Track("Drop the Game", "Flume, Chet Faker", "2013-11-12", "Lockjaw", 1923800, "asjklgmbn", "http", "id")
        track2 = Track("Landed on Mars", "Atlas Bound", "2015-03-18", "Landed on Mars",224000, "iuhmfgakuek", "http", "id")
        db.session.add(track)
        db.session.add(track2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Tests that the total # of tracks is equal to 2 (created at SetUp)
    def test_get_all_tracks(self):
        tracks = Track.query.all()
        assert len(tracks) == 2

    # Tests simple selections from the db match expected values
    def test_filtering_tracks(self):   
        track = Track.query.filter(Track.title == 'Landed on Mars').first()
        assert track.artist_name == "Atlas Bound" and track.album  == "Landed on Mars"

        track = Track.query.filter(Track.duration > 300000).first()
        assert track.artist_name == 'Flume, Chet Faker' and track.title == 'Drop the Game'   

    # Tests adding a new track to the table and then removing it
    def test_add_delete_tracks(self):
        track = Track("Where are U Now", "Jack U ,Skrillex, Diplo, Justin Bieber", "2015-02-24", "Skrillex and Diplo present Jack U", 250000, "igsjdfkjh", "http", "id")
        db.session.add(track)
        db.session.commit()
        assert len(Track.query.all()) == 3

        Track.query.filter(Track.duration > 250000).delete()
        db.session.commit()
        assert len(Track.query.all()) == 2


if __name__ == '__main__':
	unittest.main(verbosity = 2)
