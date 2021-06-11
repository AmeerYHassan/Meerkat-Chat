# The Meerkat Chat App
### By: Ameer Hassan
![meerkat_readme.png](static/meerkat_readme.png)\
[View a live demo here!](https://arcane-ravine-60026.herokuapp.com/) - **Please Note:** Due to the nature of hosting on Heroku, it may take a few refreshes and a few minutes for the website to properly load because the web server is loading up. This is only during the initial visit to the website!
## Description
This project is a simple web app that is a public chatroom. It features a bot that can call various APIs to entertain the chatters, as well as provides some utility commands. This chat room has persistence via postgresql, so any chatter will have access to the message history. A list of technolgies used include:

* [Flask](https://flask.palletsprojects.com/en/1.1.x/): A micro web framework based in Python that serves web pages.
* [React](https://reactjs.org/): The javascript frontend framework that was used to dynamically create and render the web app.
* [Postgresql](https://www.postgresql.org/): The database architecture used to implement message persistence. All messages sent to the web app is stored in the database, and is retrieved whenever a new user joins.
* [Socket.io](https://socket.io/): A library that allows for communication between web clients and servers.
* [SQLalchemy](https://www.sqlalchemy.org/): A useful ORM (Object-Relational Mapper). A database toolkit for python that translate python code to direct database statements.

## Known Problems
### User Count is not always accurate
In my implementation of this web app, whenever a new user establishes a connection to the web app, a signal is sent out via socket.io to modify a hook to add one to the user count. Whenever a user disconnects, the same hook is called specifiying to decrement the user count by one. This works for the most part, but sometimes the user count does not update, or it is just not accurate. The cause of this problem is not very apparent to me at the moment since it seems very simple, but with some more research into how react hooks work or how quickly socket.io updates the client from the server, a solution would be easy to find and implement.
### When a user inputs a bot command, the initial request is only sent to that user
When a user sends a bot command, only the output is sent to the clients, not the users original bot command. For example, if a user says `!!funtranslate this is a test for funtranslate`, the only thing the other users will see is the bot's output, not the original command declaration. Although this isn't too bad of a problem, it becomes a bit hard to follow chat when someone sends out a bot command and the original command is not shown. This could be remedied by sending out two messages from the server when a bot command is sent, a message from the bot and a message from the user. This would require a bit of refactoring in the server code, but it is absolutely doable.
### Users are sent all of the previous messages when a new user joins
When a new user joins, a signal is sent that contains a list of all of the messages that are in the database. These messages are only rendered again if a user does not already have all the messages, so on the client side nothing is different. However, on the server side, every user recieves these messages. Although it is not a problem with a small chat, it can quickly become a problem when more messages are sent and on every connection, every user recieves the whole entire message history. This can be remedied by finding a way to only send the signal to the one user using some sort of ID specific to the user.
### Python code Refactoring
Currently, `app.py` is a bit of a mess and needs some dire refactoring to make the code more readable. This can be done at any point given enough time. Some things I would want to change is to split up some of the logic to their own functions, as well as putting the bot logic into it's own class.

## Solved Technical Issues
### Postgresql and SQLalchemy
Trying to understand how to use these two technologies was not very easy. There were a lot of problems that arised ranging from the database not being created at all, to entries being input into the database the wrong way, to tables not being created, etc. All of these problems were solved by referencing online material, as well as looking at lecture slides.

### Socket listeners being created on every sent message.
This was a devastating problem for the program, and something that took a while to diagnose and debug. Whenever a message was sent, a socket listener would be added to the program. Every time a subsequent message was sent, the amount of socket listeners would double (1 &rarr; 2 &rarr; 4 &rarr; 8...). It would eventually reach to the thousands and the whole web app would come to a halt, it would take almost 10 seconds for a message to be sent on the app. After diagnosing this problem, it was fixed by removing the event listener after the message was sent, so only one would ever be present when a message is sent.

### Styling inconsistent between messages
When creating the messages and displaying on the client, I noticed that spacing between the messages was inconsistent. This had stumped me because in the css I had defined clear padding/margin for the client to follow, but it seemed to be following it's own rules. After using the developer tools to see what css the items would inherit, it became clear that for some reason, some elements were using the default padding/margin values. To overcome this, I overwrote the default styling for specific tags, like the `h1` or `div` tag.

### Messages sent to all clients when a new user joins
When a new user joined, the chat app would send all of the message history to all of the connected users. This would lead to the chat being cluttered with duplicates of the chat in the chat box. This was resolved by making a special signal for when a user first joins. When a user joins, they are sent all the messages and the client checks to make sure that the user does not have any messages before rendering all of them out.

## Milestone 2 Current Technical Issues
### Auto scroll sometimes does not work
Most of the time, the automatic scrolling of the chat window works, but sometimes it doesn't work and the user has to manually scroll down. This is a pretty hard bug to try and fix. A potential solution would be to use some different react library that handles the scrolling for me, instead of relying on the css to do it for me.

## Milestone 2 Solved Technical Issues
### Message spacing with inline images
When trying to get inline images to work, it would overlap on other message divs and cloud up the whole entire message list. Images would cover other messages and a lot of content would be missing. Diagnosing why this would happen proved to be very difficult, but it was because of the css styling and spacing. This made me take a deep dive into a few different ways of spacing in CSS, and eventually settled on the CSS grid to make the message components look elegant with a username, profile picture, and any potential inline images.

### Database appendage problems.
Initially, I thought it would be nice to just add columns to the existing database to store the new information that comes with the client authorization. This was something that I never figured out how to do elegantly. Sadly, in the end, I had to purge the entire database and recreate it from the beginning to hold all the information that I needed to store in order to render the website. The only things in my database were just test messages so nothing of value was really lost, but if this was a genuine chat room, deleting the whole entire database would upset a lot of users of the chat app.

## Milestone 2 future features
### More security with authorization
As it stands, the input and the send button are both disabled when you load into the page. If anyone is savy with HTML and the developer tools of chrome, they could go into the HTML and just undisable them. This is not very secure, as it just takes some mediocre knowledge of basic web development to bypass verification. Given more time, I would try and find a more secure way to disable the chat.

### Complete change of the site's style
The website as it is now is pretty pleasant to look at, but it is very dependent on the fact that the user is using a modern 1920x1080 monitor or larger. On smaller screens, this website is completely unusable. Given more time, I'd want to spend a lot of time on the css and just make it so things are mobile/small-screen responsive.

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
* To set up the environment variables
    - Go to the [giphy developer website.](https://developers.giphy.com/)
    - Create an account, and click the create app button
    - Choose the api option rather than the SDK option.
    - Give your app a name and description
    - Generate an API key, take note of the key.
    - Change your directory to the project directory and create a file called `api_keys.env`. In this file, add the following lines, be sure to put your own username and password for the database!\
        - `DATABASE_URL=postgresql://[USERNAME HERE]:[PASSWORD HERE]@localhost/postgres`
        - `GIPHY_KEY=<Your-Giphy-Key-Here`

To properly configure the database settings to work with our program, run the following.
* `sudo vim /var/lib/pgsql9/data/pg_hba.conf`
* In vim, run the following commands
    - `:%s/ident/md5/g`
    - `wq`
* Restart the database by running `sudo service postgresql restart`

In order to have oAuth working, you must create a valid developer account with google.
* Go to google's [developer's page.](https://console.developers.google.com/)
* Create a new project and give it an appropriate name.
* Click credentials on the side, click create credentials, and click `OAuth Client ID`.
* Select web application for application type.
* Put in your site's URL under "authorized javascript origins"
* Go to the authorized domains list and add the TLD for your website host.
* Go back to the developers website and get the client ID.
* On line 9 of `SidePanel.js`, change the client id to your client id.

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
