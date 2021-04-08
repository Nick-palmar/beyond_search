from flask import render_template,send_from_directory,request, jsonify, make_response, send_static_file
import os
from models import app, db, ma, RepoSchema, RepoStrings, serialize_search_results
# from flask_cors import cross_origin
from trie import Trie
from typing import List
from sqlalchemy import and_
import requests
import json

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

def set_trie(new_trie: Trie, reset=False) -> None:
    """Private helper function to set the trie in memory"""
    if not reset:
        if len(get_trie()) == 0:
            get_trie().append(new_trie)
        else:
            get_trie().pop()
            get_trie().append(new_trie)
    else:
        _trie_version = []

def create_trie_from_db() -> None:
    # create the trie by looking at DB repo strings
    repo_trie = Trie()
    repos = RepoStrings.query.all()
    for repo_obj in repos:
        repo_trie.insert(repo_obj.repo)
    # store the trie in memory for use
    set_trie(repo_trie)

def should_create_trie() -> bool:
    # see if a trie can be created from the db
    all_repos = RepoStrings.query.all()
    trie = get_trie()
    return len(all_repos) > 0 and trie == []

@app.route('/')
def serve():
    return app.send_static_file('index.html')

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')

@app.route('/api/create-trie', methods=['GET'])
# @cross_origin()
def create_trie():
    try:
        create_trie_from_db()
        # loop through each repo, take the strings and add to the try
        return jsonify({'Success': 'Trie Created'}), 200
    except Exception as e:
        # error occured while creating trie 
        return jsonify({'Error': f'Occured while making trie, {e}'}), 400


@app.route('/api/add-user', methods=['POST'])
# @cross_origin()
def add_user():
    user_name = request.form.get('userName')

    # check if the user exists in the db, if not insert
    if db.session.query(RepoStrings).filter(RepoStrings.user_name==user_name).first() == None:
        # add the user's repos to the db  
        try:
            # call the github API to get repo info - first parse info for only repo names
            api_string = f'https://api.github.com/users/{user_name}/repos'
            repo_info = requests.get(api_string).json()
            print(len(repo_info))
            
            # the repo info will be a list of dict if the username is found
            if type(repo_info) == list:
                # if should_create_trie():
                #     create_trie_from_db()
                # get the current trie to update in the loop 
                curr_trie = get_trie()[0]
                for dictionary in repo_info:
                    print(dictionary.get('name'))
                    repo_name = dictionary.get('name').lower()
                    # for each repo name, add to db with user name and insert repo into tree
                    new_repo = RepoStrings(repo_name, user_name)
                    db.session.add(new_repo)

                    # add the name to the trie, which updates the trie in memory
                    print(repo_name)
                    curr_trie.insert(repo_name)
                    # print(dictionary.get('name'))
            # username was not found
            else:
                return jsonify({'Not Found': 'User was not found'}), 404

            # commit once process completes
            db.session.commit()

            return jsonify({'Success': 'User\'s repos added'}), 201
        except Exception as e:
            # error occured in insertion/creation
            db.session.rollback()
            return jsonify({'Bad Request': f'Error inserting user, {e}'}), 400

    else:
        return ({'Success': 'User already exists'}), 200

@app.route('/api/search-trie', methods=['GET'])
# @cross_origin()
def search_trie():
    search_string = request.args.get('searchString')

    # check if the search string is empty; return none
    if search_string == '' or search_string == None:
        return jsonify([]), 200

    try:
        # see if a trie can be created from the db
        # if should_create_trie():
        #     create_trie_from_db()
        #     print('trie created')
        # get the current trie  
        curr_trie = get_trie()
        if len(curr_trie) != 0:
            curr_trie = curr_trie[0]
            # get the search results by applying the trie and serialize the results
            search_result_list = curr_trie.find_all_strings(search_string)

            # deal with entries that are none
            if search_result_list == None:
                return jsonify([]), 200
            # sort the list by length to return the shortest results first
            search_result_list = sorted(search_result_list, key=len)
            print(search_result_list)
            # loop through each repo and search in db
            serialized_search_results = []
            index = 1
            for repo in search_result_list:
                repo_records = RepoStrings.query.filter_by(repo=repo).all()

                # loop through repos to create return list
                for repo_record in repo_records:
                    serialized_search_results.append({'id': index, 'repoName': repo_record.repo, 'userName': repo_record.user_name})
                    index += 1

            # print(serialized_search_results)
            # serialized_search_list = serialize_search_results(search_result_list)
            return jsonify(serialized_search_results), 200
        else:
            # no trie is selected
            return jsonify([]), 200
    
    except Exception as e:
        # invalid search character entered
        return jsonify({'Error': f'{e}'}), 400


@app.route('/api/truncate/<secret_key>', methods=['DELETE'])
# @cross_origin()
def delete_all(secret_key):
    if secret_key == '8':
        # secret key is correct, delete all from db
        RepoStrings.query.delete()
        db.session.commit()
        set_trie(Trie(), reset=True)
        return '', 204
    
    return jsonify({'Unauthorized': 'Secret delete key incorrect, unable to truncate table'}), 403

@app.route('/api/github', methods=['GET'])
def test_github():
    github_name = request.args.get('userName')

    api_string = f'https://api.github.com/users/{github_name}/repos'
    print(api_string)
    repo_info = requests.get(api_string).json()
    # print(repo_info)
    # dict_repo = json.loads(repo_info)
    # print(repo_info)
    if type(repo_info) == list:
        for dictionary in repo_info:
            print(dictionary.get('name'))
    else:
        print(repo_info.get('message'))
    return jsonify(repo_info)

@app.route('/api/test-insert')
# @cross_origin()
def test_insert():
    repo = RepoStrings('test-insert', 'user1')
    db.session.add(repo)
    db.session.commit()
    serialized_repo = repo_schema.dump(repo)
    return jsonify(serialized_repo)

@app.route('/api/get-all', methods=['GET'])
# @cross_origin()
def get_all_repos():
    repos = RepoStrings.query.all()
    db.session.commit()
    serialized_repos = multiple_repo_schema.dump(repos)
    return jsonify(serialized_repos)

if __name__ == '__main__':
    app.run(debug=True)

