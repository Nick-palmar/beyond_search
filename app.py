from flask import render_template,send_from_directory,request, jsonify, make_response
import os
from models import app, db, ma, RepoSchema, RepoStrings, serialize_search_results
from flask_cors import cross_origin
from trie import Trie
from typing import List

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
_trie_version = []

def get_trie() -> List[Trie]:
    return _trie_version

def set_trie(new_trie: Trie) -> None:
    """Private helper function to set the trie in memory"""
    if len(get_trie()) == 0:
        get_trie().append(new_trie)
    else:
        get_trie().pop()
        get_trie().append(new_trie)

@app.route('/api/create-trie', methods=['GET'])
@cross_origin()
def create_trie():
    try:
        # create the trie by looking at DB repo strings
        repo_trie = Trie()
        repos = RepoStrings.query.all()
        for repo_obj in repos:
            repo_trie.insert(repo_obj.repo)
        # store the trie in memory for use
        set_trie(repo_trie)
        # loop through each repo, take the strings and add to the try
        return jsonify({'Success': 'Trie Created'}), 200
    except Exception as e:
        # error occured while creating trie 
        return jsonify({'Error': f'Occured while making trie, {e}'}), 400


@app.route('/api/add-repo', methods=['POST'])
@cross_origin()
def add_repo():
    repo_name = request.form.get('repoName')

    # check if the repo exists in the db, if not insert it
    if RepoStrings.query.filter_by(repo=repo_name).first() == None:
        # add the repo to the db  
        try:
            new_repo = RepoStrings(repo_name)
            db.session.add(new_repo)

            # add the name to the trie, which updates the trie in memory
            curr_trie = get_trie()[0]
            curr_trie.insert(repo_name)
            db.session.commit()

            return jsonify({'Success': 'Repo added'}), 201
        except Exception as e:
            # error occured in insertion/creation
            db.session.rollback()
            return jsonify({'Bad Request': f'Error inserting repo, {e}'}), 400

    else:
        return ({'Success': 'Repo already exists'}), 200

@app.route('/api/search-trie', methods=['GET'])
@cross_origin()
def search_trie():
    search_string = request.args.get('searchString')

    # get the current trie  
    curr_trie = get_trie()

    try:
        if len(curr_trie) != 0:
            curr_trie = curr_trie[0]
            # get the search results by applying the trie and serialize the results
            search_result_list = curr_trie.find_all_strings(search_string)
            serialized_search_list = serialize_search_results(search_result_list)
            return jsonify(serialized_search_list), 200
        else:
            # no trie is selected
            return jsonify({}), 200
    
    except Exception as e:
        # invalid search character entered
        return jsonify({'Error': f'{e}'}), 400


@app.route('/api/truncate/<secret_key>', methods=['DELETE'])
@cross_origin()
def delete_all(secret_key):
    if secret_key == '8':
        # secret key is correct, delete all from db
        RepoStrings.query.delete()
        db.session.commit()
        set_trie(Trie())
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

@app.route('/api/get-all', methods=['GET'])
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

