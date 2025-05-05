from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Artist(db.Model):
    __tablename__ = 'Artist'
    ArtistId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)

class Album(db.Model):
    __tablename__ = 'Album'
    AlbumId = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String)
    ArtistId = db.Column(db.Integer, db.ForeignKey('Artist.ArtistId'))
    
    artist = db.relationship('Artist', backref='albums')
