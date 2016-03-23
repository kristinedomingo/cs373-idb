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

    def test_get_all_prizes(self):
        artists = Artist.query.all()
        assert len(Artist) == 2

    def test_filtering_prizes(self):   
        artists = Artist.query.filter_by(category == 'Lullaby').first()
        assert artist.name == "Atlas Bound" && artist.popularity  == 42

        artists = Artist.query.filter_by(popularity < 47).first()
        assert artist.name == 'Chet Faker' && artist.recent_album == 'Drop the Game'   

    def test_add_delete_prizes(self):
        artists = Artist("Jack U", 14, "Skrillex and Diplo present Jack U", "Where Are U Now ( with Justin Bieber )", 42)
        db.session.add()
        db.session.commit()
        assert len(Artist.query.all()) == 3

        Artist.query.filter_by(artist == 'Jack U').delete()
        db.session.commit()
        assert len(Artist.query.all()) == 1 

if __name__ == '__main__':
	unittest.main()