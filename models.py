from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from decouple import config
# from flask_cors import CORS
from typing import List, Dict
from flask_migrate import Migrate

# set up the app 
app = Flask(__name__, static_folder='client/build', static_url_path='')
# cors = CORS(app)
db_uri = config('DB_URL').replace("://", "ql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri 

# add flask-sql alchemy for db and marshmallow to serialize the data
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

class RepoStrings(db.Model):
    __tablename__ = "RepoStrings"
    # __table_args__ = {'extend_existing': True}
    repo_id = db.Column(db.Integer, primary_key=True)
    repo = db.Column(db.String(80), nullable=False)
    user_name = db.Column(db.String, nullable=False)

    def __init__(self, repo: str, user_name: str) -> None:
        """Create a new repo string object"""
        self.repo = repo
        self.user_name = user_name

class RepoSchema(ma.Schema):
    class Meta:
        fields=('repo_id', 'repo', 'user_name')

def serialize_search_results(search_list: List[str]) -> Dict[int, str]:
    serialized_dict = {}

    # loop through and serialize the list
    for i in range(len(search_list)):
        serialized_dict[i+1] = search_list[i]
    print(serialized_dict)
    return serialized_dict
