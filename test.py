import unittest
from flask.ext.testing import TestCase
import Datetime
import db from app
class TestArtist(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
        return app

    def setUp(self):
        db.create_all()
        artist = Artist("Atlas Bound", 8, "Lullaby", "Landed on Mars", 42)
        artist2 = Artist("Chet Faker", 20, "1998 Melbourne Edition", "Drop the Game",76)
        db.session.add(artist)
        db.session.add(artist2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_all_artist(self):
        artists = Artist.query.all()
        assert len(artists) == 2

    def test_filtering_artist(self):   
        artists = Artist.query.filter_by(category == 'Lullaby').first()
        assert artist.name == "Atlas Bound" && artist.popularity  == 42

        artists = Artist.query.filter_by(popularity < 47).first()
        assert artist.name == 'Chet Faker' && artist.recent_album == 'Drop the Game'   

    def test_add_delete_artist(self):
        artists = Artist("Jack U", 14, "Skrillex and Diplo present Jack U", "Where Are U Now ( with Justin Bieber )", 42)
        db.session.add()
        db.session.commit()
        assert len(Artist.query.all()) == 3

        Artist.query.filter_by(artist == 'Jack U').delete()
        db.session.commit()
        assert len(Artist.query.all()) == 1 

class TestAlbum(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
        return app

    def setUp(self):
        db.create_all()
        album = Album("1998 Melbourne Edition", "Chet Faker", 2015-05-18, 1923800, 5)
        album = Album("Lullaby", "Atlas Bound", 2016-03-18, 220000,1)
        db.session.add(artist)
        db.session.add(artist2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_all_albums(self):
        album = Album.query.all()
        assert len(album) == 2

    def test_filtering_album(self):   
        album = Album.query.filter_by(name == 'Lullaby').first()
        assert album.artist_name == "Atlas Bound" && album.num_tracks  == 1

        album = Artist.query.filter_by(num_tracks > 2).first()
        assert album.artist_name == 'Chet Faker' && album.name == '1998 Melbou Edition'   

    def test_add_delete_album(self):
        album = Album( "Skrillex and Diplo present Jack U", 2015-02-24, 2125000, 10)
        db.session.add()
        db.session.commit()
        assert len(Album.query.all()) == 2

        Album.query.filter_by(length < 2125000).delete()
        db.session.commit()
        assert len(Album.query.all()) == 1 


class TestTrack(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
        return app

    def setUp(self):
        db.create_all()
        track = Track("Drop the Game", "Flume, Chet Faker",2013-11-12, "Lockjaw", 1923800, )
        track2 = Track("Landed on Mars", "Atlas Bound", 2015-03-18, "Landed on Mars",224000)
        db.session.add(track)
        db.session.add(track2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_all_tracks(self):
        tracks = Track.query.all()
        assert len(tracks) == 2

    def test_filtering_tracks(self):   
        track = Track.query.filter_by(name == 'Landed on Mars').first()
        assert track.artist_name == "Atlas Bound" && track.album  == "Landed on Mars"

        track = Track.query.filter_by(duration > 300000).first()
        assert track.artist_name == 'Flume, Chet Faker' && track.name == 'Drop the Game'   

    def test_add_delete_tracks(self):
        track = Track("Where are U Now", "Jack U ,Skrillex, Diplo, Justin Bieber", 2015-02-24, "Skrillex and Diplo present Jack U",2015-02-24, 250000)
        db.session.add()
        db.session.commit()
        assert len(Track.query.all()) == 2

        Tracks.query.filter_by(duration == 250000).delete()
        db.session.commit()
        assert len(Track.query.all()) == 1 




if __name__ == '__main__':
	unittest.main()