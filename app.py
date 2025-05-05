from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask import request, jsonify
from model import db, Artist, Album

pymysql.install_as_MySQLdb()

# Initialize Flask app
app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:teja@localhost/chinook_autoincrement'  # Adjust with your credentials and database name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional but recommended to disable Flask's modification tracking

db.init_app(app)


@app.route('/albums/search', methods=['GET'])
def search_albums():
    query = request.args.get('q')

    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    if query.isdigit():
        # Treat as artist ID
        albums = Album.query.filter_by(ArtistId=int(query)).all()
    else:
        # Treat as artist name
        artist = Artist.query.filter(Artist.Name.ilike(f"%{query}%")).first()
        if not artist:
            return jsonify({"error": "Artist not found"}), 404
        albums = Album.query.filter_by(ArtistId=artist.ArtistId).all()

    return jsonify([
        {"AlbumId": album.AlbumId, "Title": album.Title, "ArtistId": album.ArtistId}
        for album in albums
    ])

@app.route('/add_album/<int:artist_id>', methods=['POST'])
def add_album(artist_id):
    title = request.json.get('title')
    
    # Create a new album with the provided artistId
    new_album = Album(Title=title, ArtistId=artist_id)
    
    db.session.add(new_album)
    db.session.commit()
    return jsonify(message=f"Album '{title}' added for artist {artist_id}"), 200



# Route to test database connection
@app.route('/')
def index():
    return "Hello, Flask with SQLAlchemy!"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
