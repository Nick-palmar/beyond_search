from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from flask_cors import CORS

# set up the app 
app = Flask(__name__, static_folder='client/build', static_url_path='')
cors = CORS(app)
db_uri = config('DB_URL').replace("://", "ql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri 

# add flask-sql alchemy for db and marshmallow to serialize the data
db = SQLAlchemy(app)
ma = Marshmallow(app)

class RepoStrings(db.Model):
    __tablename__ = "RepoStrings"
    __table_args__ = {'extend_existing': True}
    repo_id = db.Column(db.Integer, primary_key=True)
    repo = db.Column(db.String(80), nullable=False)

    def __init__(self, repo: str) -> None:
        """Create a new repo string object"""
        self.repo = repo

class RepoSchema(ma.Schema):
    class Meta:
        fields=('repo_id', 'repo')
        
