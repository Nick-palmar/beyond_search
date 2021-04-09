# Beyond Search

Beyond Search is a web application for performing group searches on github user's repos. 

***

## Motivation

This project was created as part of the Manulife hackathon. It attempts to tackle the 3rd problem statement which is about expanding the limited search functionalities on github. 
I took a twist on this idea to make it useful for both managers and regular users. Managers can use the 
application to add new coop students and search by repo to see who has access to what repo. Regular users can simply add other github users and search by repo, allowing for a 'group'
search to be made. This way, you can find out about what other users are working on by repo name - and see if that is something you want to look more into!

***

## Tech/framework
**Built with**
- Flask (Python)
- SQLAlchemy (Python ORM - for the database)
- Pandas (Python)
- Github API (For finding repos)
- React (Javascript, Jsx/HTML, CSS)
- Material UI
- Heroku (Cloud hosting)

## Features
The repo searching algorithm in the backend makes use of a data struture called a **[trie](https://en.wikipedia.org/wiki/Trie)**. The data structure itself was not too difficult to implement but I had to come up with the searching algorithm (depending on what the user has entered as the current input). The algorithm uses a **recursive function** to return all repos from a certain node. This way, the search algorithm is optimized for speed. 

***


## Demo
 See usage tips below for help 

**Web Application**: <https://beyond-search.herokuapp.com/main>


## Screenshots
This is the main web application page
![alt text](https://github.com/Nick-palmar/beyond_search/blob/main/images/beyond_search_main.png "Beyond Search UI")

## Usage
1. To add a user, type in their exact user name and press *add*. You will recieve a pop up telling you if the user was added or not.
2. To search for repos, start typing the repo names in the search bar - the results should update in live time!
3. To clear all the results from the database (clear all users and repos), click the trash can in the top right corner of the *add* card. 

*General advice*
1. If the github username is valid and not loading, refresh the application and try again
2. For better results, type slower in the search bar (to avoid making too many backend calls all at the same time)

***


## Authors
This project was actually made solo in 36h. Note: Writing the frontend, backend, and learning a new data structure with a complex searching algorithm is not easy to pull off in such a short time.. but I finished!