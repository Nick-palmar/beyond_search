from flask import render_template,send_from_directory,request, jsonify, make_response
import boto3
import os
from models import app, db, ma, RepoSchema, RepoStrings
from flask_cors import cross_origin
from trie import Trie

# set up the app
# app = Flask(__name__, static_folder='client/build', static_url_path='')
# cors = CORS(app)
# db_uri = config('DB_URL').replace("://", "ql://", 1)
# app.config['SQLALCHEMY_DATABASE_URI'] = db_uri 
# db = SQLAlchemy(app)
db.create_all()
db.session.commit()

repo_schema = RepoSchema()
multiple_repo_schema = RepoSchema(many=True)
repo_trie = None

@app.route('/api/create-trie', methods=['GET'])
@cross_origin()
def create_trie():
    try:
        # create the trie by looking at DB repo strings
        repo_trie = Trie()
        repos = RepoStrings.query.all()
        for repo_obj in repos:
            repo_trie.insert(repo_obj.repo)

        # loop through each repo, take the strings and add to the try
        return jsonify({'Success': 'Trie Created'}), 200
    except Exception as e:
        # error occured while creating trie 
        return jsonify({'Error': f'Occured while making trie, {e}'}), 400


@app.route('/api/truncate/<secret_key>', methods=['DELETE'])
@cross_origin()
def delete_all(secret_key):
    if secret_key == '8':
        # secret key is correct, delete all from db
        RepoStrings.query.delete()
        db.session.commit()
        return '', 204
    
    return jsonify({'Unauthorized': 'Secret delete key incorrect, unable to truncate table'}), 403


@app.route('/api/test-insert')
@cross_origin()
def test_insert():
    repo = RepoStrings('test-insert')
    db.session.add(repo)
    db.session.commit()
    serialized_repo = repo_schema.dump(repo)
    return jsonify(serialized_repo)

@app.route('/api/get-all')
@cross_origin()
def get_all_repos():
    repos = RepoStrings.query.all()
    serialized_repos = multiple_repo_schema.dump(repos)
    return jsonify(serialized_repos)

# @app.route('/')
# def serve():
#     return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)