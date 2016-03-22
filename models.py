

artists = db.Table('artists',
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')),
    db.Column('album_id', db.Integer, db.ForeignKey('album.id')))

artists2= db.Table('artists2',
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')),
    db.Column('track_id', db.Integer, db.ForeignKey('track.id')))

class Album(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    date = db.Column(db.DateTime)
    length = db.Column(db.Integer)
    num_tracks = db.Column(db.Integer)
    artists = db.relationship('Artist', secondary=artists,
        backref=db.backref('albums', lazy='dynamic'))

    def __init__(self, name, date, length, num_tracks ):
        self.name = name
        self.date = date
        self.length= length
        self.num_tracks=num_tracks


	def __repr__(self):
        return '<User %r>' % self.username

class Artist(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    num_albums = db.Column(db.Integer)
    recent_album= db.Column(db.String(100))
    top_track = db.Column(db.String(100))
    popularity = db.Column(db.Integer)
    
    def __init__(self, name, num_albums, recent_album, top_track, popularity ):
        self.name = name
        self.num_albums = num_albums
        self.recent_album= recent_album
        self.top_track=top_track
        self.popularity=popularity

    def __repr__(self):
        return '<User %r>' % self.name


class Track(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    num_albums = db.Column(db.Integer)
    recent_album= db.Column(db.String(100))
    top_track = db.Column(db.String(100))
    popularity = db.Column(db.Integer)
    artists2 = db.relationship('Artist', secondary=artists2,
        backref=db.backref('tracks', lazy='dynamic'))

    def __init__(self, name, num_albums, recent_album, top_track, popularity ):
        self.title = name
        self.num_albums = num_albums
        self.recent_album= recent_album
        self.top_track=top_track
        self.popularity=popularity

    def __repr__(self):
        return '<User %r>' % self.name
