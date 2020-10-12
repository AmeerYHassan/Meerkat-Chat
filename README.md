# The Meerkat Chat App
### By: Ameer Hassan
![meerkat_readme.png](static/meerkat_readme.png)\
[View a live demo here!](https://cryptic-shore-24355.herokuapp.com/)
## Description
This project is a simple web app that is a public chatroom. It features a bot that can call various APIs to entertain the chatters, as well as provides some utility commands. This chat room has persistence via postgresql, so any chatter will have access to the message history. A list of technolgies used include:

* [Flask](https://flask.palletsprojects.com/en/1.1.x/): A micro web framework based in Python that serves web pages.
* [React](https://reactjs.org/): The javascript frontend framework that was used to dynamically create and render the web app.
* [Postgresql](https://www.postgresql.org/): The database architecture used to implement message persistence. All messages sent to the web app is stored in the database, and is retrieved whenever a new user joins.
* [Socket.io](https://socket.io/): A library that allows for communication between web clients and servers.
* [SQLalchemy](https://www.sqlalchemy.org/): A useful ORM (Object-Relational Mapper). A database toolkit for python that translate python code to direct database statements.

## Known Problems
### User Count is not always accurate.
In my implementation of this web app, whenever a new user establishes a connection to the web app, a signal is sent out via socket.io to modify a hook to add one to the user count. Whenever a user disconnects, the same hook is called specifiying to decrement the user count by one. This works for the most part, but sometimes the user count does not update, or it is just not accurate. The cause of this problem is not very apparent to me at the moment since it seems very simple, but with some more research into how react hooks work or how quickly socket.io updates the client from the server, a solution would be easy to find and implement.
### Chat window does not scroll automatically.
The chat window is in it's own div element, and the div element has it's own scroll bar so the whole body isn't extended out when messages get sent. Despite this, the user has to continually scroll down in the div to see the most recent messages. Although this is a small problem, it is a bit annoying to continually scroll down to read the latest messages. I have tried to redemy this problem by using some vanilla javascript to keep the div scrolled down, but nothing has worked so far. This could potentially be fixed through some react libraries that I could include in my project, as there are a few that strictly concern themselves with scrolling.
### Bot commands are not sent to other clients.
When a user sends a bot command, only the output is rendered and sent back. Although this isn't too bad of a problem, it becomes a bit hard to follow chat when someone sends out a bot command and the original command is not shown. This could be remedied by sending out two messages from the server when a bot command is sent, a message from the bot and a message from the user. This would require a bit of refactoring in the server code, but it is absolutely doable.
### Messages are sent after a new user joins to all users.
When a new user joins, the server sends out all of the messages in the database to all of the users, even if the user already holds all of the messages. Something I did to try and combat this problem was to only send an array containing all of the messages to newly joined user on their own signal using socket.io, but this ran into some problems when creating the react app since the array held objects. In order to fix this problem in the future, I plan on trying to find a different way to send these messages using a different method.
### Python code Refactoring
Currently, `app.py` is a bit of a mess and needs some dire refactoring to make the code more readable. This can be done at any point given enough time. Some things I would want to change is to split up some of the logic to their own functions, as well as putting the bot logic into it's own class.

## Solved Technical Issues
### Postgresql and SQLalchemy
Trying to understand how to use these two technologies was not very easy. There were a lot of problems that arised ranging from the database not being created at all, to entries being input into the database the wrong way, to tables not being created, etc. All of these problems were solved by referencing online material, as well as looking at lecture slides.

### Socket listeners being created on every sent message.
This was a devastating problem for the program, and something that took a while to diagnose and debug. Whenever a message was sent, a socket listener would be added to the program. Every time a subsequent message was sent, the amount of socket listeners would double (1 &rarr; 2 &rarr; 4 &rarr; 8...). It would eventually reach to the thousands and the whole web app would come to a halt, it would take almost 10 seconds for a message to be sent on the app. After diagnosing this problem, it was fixed by removing the event listener after the message was sent, so only one would ever be present when a message is sent.

### Styling inconsistent between messages
When creating the messages and displaying on the client, I noticed that spacing between the messages was inconsistent. This had stumped me because in the css I had defined clear padding/margin for the client to follow, but it seemed to be following it's own rules. After using the developer tools to see what css the items would inherit, it became clear that for some reason, some elements were using the default padding/margin values. To overcome this, I overwrote the default styling for specific tags, like the `h1` or `div` tag.

## How to deploy
To run your own local version of this chat app:
* Run `git clone https://github.com/NJIT-CS490/project2-m1-ayh7`, and `cd` into your directory.
* In the terminal, run the following commands to install all the dependencies
    - `npm install`
    - `pip install flask`
    - `pip install flask-socketio`
    - `pip install eventlet`
    - `npm install -g webpack`
    - `npm install --save-dev webpack`
    - `npm install socket.io-client --save`
* In order to link the database to python, run the following
    - `sudo yum update`, say yes to all prompts
    - `sudo pip install --upgrade pip`
    - `sudo pip install psycopg2-binary`
    - `sudo pip install Flask-SQLAlchemy==2.1`
* To install and set up the database, run the following
    - `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`, say yes to all of the prompts
    - `sudo service postgresql initdb`
    - `sudo service postgresql start`
    - `sudo -u postgres createuser --superuser $USER`
    - `sudo -u postgres createdb $USER`
    - `psql`
    - You are going to be creating a user here, keep in mind the username and password!
        - `create user [USERNAME HERE] superuser password '[PASSWORD HERE]';`
        - `\q`

Change your directory to the project directory and create a file called `sql.env`. In this file, add the following line, be sure to put your own username and password!\
`DATABASE_URL=postgresql://[USERNAME HERE]:[PASSWORD HERE]@localhost/postgres`

To properly configure the database settings to work with our program, run the following.
* `sudo vim /var/lib/pgsql9/data/pg_hba.conf`
* In vim, run the following commands
    - `:%s/ident/md5/g`
    - `wq`
* Restart the database by running `sudo service postgresql restart`

To run the app, type `npm run watch` in a terminal, and in a seperate terminal type `python app.py`.

To deploy to heroku:
* Login to Heroku using `heroku login -i` in the console.
* Use `heroku create` to create a new app.
* Use `heroku addons:create heroku-postgresql:hobby-dv` to install heroku dependencies.

If you want to add your local database changes:
* Use `heroku pg:wait` to begin the process of transferring your local database to heroku
* Type `PGUSER=<db username> heroku pg:push postgres DATABASE_URL`
* Enter your database password when prompted.

Lastly, 
* Push your project to heroku using `git push heroku master`