# Xweeter App

A simple social media app built using Vue and Flask.

## Background Scenario

A web developer has been instructed to create a social media platform that resembles Twitter but is simpler and more intuitive.

## Requirements

The social media app should have the following features:

1. User authentication
2. Users can add, edit, or delete a tweet.
3. Users can upload an image and attach it to a tweet.
4. Users can interact with other users' tweet, such as giving them a like.
5. Users can view the count of likes on each tweet.
6. Users can view a list that displays the most active users of the day.
7. The admin has a special access to the admin page.
8. There is a simple pagination feature to retrieve more tweets when necessary.

## Program Scheme

![A flowchart image that explains how the program runs](docs/user-journey-flowchart.jpg)

### START

1. Users create an account if they don't already have one, then log in.
2. Unauthenticated users can only view timeline that consists of tweets from all users.
3. Authenticated users can view a personalized timeline based on the users they already follow.
4. Authenticated users can send new tweets and also edit or delete existing tweets.
5. Authenticated users can interact with other users' tweets such as giving them a like.
6. All users can view the leaderboard that displays the most active users of the day.
7. Authenticated users with the admin role have special access to the admin page.

### END

## Demo

<https://mad4869.pythonanywhere.com>

## ERD

This app utilizes __PostgreSQL__ as the database service. The structure of the schema in the database is as follows:
![Entity Relationship Diagram](docs/erd.png)

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/mad4869/todo-app.git
```

### 2. Set up the enviromental variables

Create a new file named `.env` in the root directory of the app. Then, inside the `.env` file, add the required variables:

```env
FLASK_APP='run.py'
FLASK_DEBUG=1
ENVIRONMENT="development"
SECRET_KEY="some_secret_key"

POSTGRES_USER="postgres"
POSTGRES_PASSWORD="password"
POSTGRES_HOST="localhost"
POSTGRES_PORT="5432"
POSTGRES_DB="todo-db"

JWT_SECRET_KEY="some_secret_key"
```

Replace the example variables with the corresponding actual values as needed.

### 3. Create a virtual environment (optional)

### 4. Install the dependencies

```bash
pip install -r requirements.txt
npm install
```

### 5. Build the static assets

```bash
npm run build
flask digest compile
```

### 6. Connect to the database

```bash
flask db init
flask db migrate
flask db upgrade
```

### 7. Run the app

```bash
flask run
```

## Code Explanation

### 1. Backend

The backend is built using the __Flask__ framework to serve REST API to the clients through various endpoints. The entry point is `run.py` inside the `server` directory. The app utilizes several supporting libraries, including:

- `SQLAlchemy` for object-relational mapping (ORM).
- `flask-migrate` to manage database migrations.
- `flask-bcrypt` for generating password hashes.
- `flask-jwt-extended` for authentication and authorization using JSON Web Tokens (JWT).

Inside the todo module, the following files are present:

- `__init__.py:` Initialization file.
- `config.py:` App configuration.
- `extensions.py:` Initialization file for the app's supporting libraries.

The `server` also includes the following directories:

#### routes

- `api:` Handling the routes that serve the data. The list of API endpoints can be viewed [here.](https://documenter.getpostman.com/view/11633108/2s93zH2eWg)
- `auth:` Handling the routes for authentication.
- `views:` Handling the routes for rendering HTML templates.

#### static

Contains all the static assets (e.g., CSS, JavaScript, images).

#### templates

Contains HTML templates used for rendering web pages.

### 2. Frontend

The frontend is built using __Vue__ as the Javascript framework and __Tailwind CSS__ as the CSS framework.

## Test Case

### 1. User authentication

![User login](docs/test/login.png)
![User login successfully](docs/test/login_success.png)

### 2. Send a new tweet

![Send a tweet](docs/test/new_xweet.png)
![Send a tweet from modal](docs/test/new_xweet_modal.png)
![Send a tweet successfully](docs/test/new_xweet_successful.png)

### 3. Edit a tweet

![Edit a tweet](docs/test/edit_xweet.png)
![Show the tweet editor](docs/test/edit_xweet_editor.png)
![Edit a tweet successfully](docs/test/edit_xweet_success.png)
![The tweet that has been edited](docs/test/edited_xweet.png)

### 4. Delete a tweet

![Delete a tweet](docs/test/delete_xweet.png)
![Show the delete modal](docs/test/delete_xweet_modal.png)
![Delete a task successfully](docs/test/delete_xweet_success.png)

### 5. Upload an image and attach it to a tweet

![Send a tweet with picture](docs/test/upload_image.png)
![Send a tweet with picture successfully](docs/test/upload_image_success.png)

### 6. Like a tweet and view the count of the likes

![Like a tweet](docs/test/like_xweet.png)
![Like a tweet successfully and view the count increases](docs/test/like_xweet_success.png)

### 7. Leaderboard for most active users

![Leaderboard](docs/test/leaderboard.png)

### 8. Admin page for user with admin role

![Admin page](docs/test/admin_page.png)

### 9. Retrieve more tweets when necessary

![More tweets](docs/test/more_xweet.png)
![More tweets loaded](docs/test/more_xweet_success.png)

## Conclusion

TODO is a simple to-do app that allows users to track their tasks or projects. However, there are a few things that can be done to enhance the app:

1. Implement task pagination to improve the user experience.
2. Optimize the static files to enhance the app's performance.
3. Clean up the code to improve its overall readability.

By implementing these improvements, the overall functionality and performance of the app can be enhanced.
