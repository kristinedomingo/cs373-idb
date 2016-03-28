#!flask/bin/python
from app.idb import db
from models import Artist, Track, Album


db.create_all()
artist = Artist("Atlas Bound", 8, "Lullaby", "Landed on Mars", 42, "alsjdflkasjd", "http")

db.session.add(artist)

db.session.commit()




if __name__ == "__main__":
	print("hello")