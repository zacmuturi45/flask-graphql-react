# Script 1


## 🚀 Getting Started/Installations & Setup

To get our project up and running, follow the guidelines below. These guidelines assumes you have `Python`, `Node.js` and `npm` installed on your system

### 1. Create a Project Directory

First, create a new project directory, let's call it 'Bots', cd into it and initiate an Git repository

```bash
mkdir Bots
cd Bots
git init
```

Our project directory will contain the front end and back end sub-directories. 

### 2. Creating the Front end

Let's create the front end directory with npm
```bash
npx create-react-app frontend
```

### 3. Create the Back end

Create the 'backend' directory, cd into it, create a new python directory and activate the virtual environment.

```bash
mkdir backend
cd backend
python3 -m venv venv
source venv/bin/activate
```

*Create the following files*

```bash
touch __init__.py .env .gitignore app.py config.py setup.py
mkdir src
cd src
touch __init__.py models.py schema.py seed.py
cd ..
```

### Explanations
- ```__init__.py``` : This is a python file that indicates that the directory containing it should be treated as a Python package. Without it, Python will not recognize the directory as a package and its modules will not be accessible through imports from the package
- ```.env``` : .env files are used to store environment variables. Passwords, secret words and any sensitive information is stored here, and the file added to our gitignore file to avoid it being pushed to github.
- ```.gitignore```: Used to list files that git should skip when pushing to your github repo.
-```config.py```:  Here is where we will store all our configuration code for the application
-```setup.py```: Here we will configure our setuptools code to manage and distribute our python code. The main purpose of this file is to automatically discover all the packages and modules in our project, reducing the need to manually list them as we will see.
-```models.py```: Contains the structure of our database tables and relationships.
-```schema.py```: This is where we will define our GraphQL schema. We will be specifying the types, queries and mutations available for your API.
-```app.py```: Sets up our Flask application, this is where we initialize our application by using our defined models, schema and configurations.

### Installations

We will install the following dependencies and add them to our requirements.txt file.

```bash
pip install flask flask_cors flask_migrate flask_graphql faker setuptools python-dotenv black

pip freeze > requirements.txt
```

### Explanation

- **`flask`**: Our chosen Python framework for building our application.
- **`flask_cors`**: Provides Cross-Origin Resource Sharing (CORS) support for Flask applications. It simply gives the front end permission to query the back end.
- **`flask_migrate`**: Handles our SQLAlchemy database migrations.
- **`flask_graphql`**: Integrates GraphQL with Flask, allowing us to build GraphQL APIs.
- **`faker`**: Generates fake data for testing or populating our database with dummy content.
- **`setuptools`**: A library for packaging Python projects, including installation and distribution. 
- **`python-dotenv`**: This enables us to read our environment variables from the `.env` file we used for managing configuration settings.
- **`black`**: An automatic code formatter for Python that enforces a consistent style. 

## Add the following to your gitignore file

```bash
.env

# Python
*.pyc
__pycache__/
*.pyo
*.pyd
*.pyc
*.pyo
*.pyz
*.pyzw
*.py[cod]

# virtual environments
venv/
env/
ENV/

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDEs
.idea/
.vscode/.env
```

### `.gitignore` Explanations

- **`.env`**: Excludes environment variable files which contain sensitive information such as API keys and configuration details.

- **Python Files**:
  - `*.pyc`: Compiled Python files, which are generated during the execution of Python code.
  - `__pycache__/`: Directory where Python stores compiled bytecode files.
  - `*.pyo`, `*.pyd`, `*.pyz`, `*.pyzw`: Other compiled or packaged Python files.
  - `*.py[cod]`: Includes multiple variations of compiled Python files.

- **Virtual Environments**:
  - `venv/`, `env/`, `ENV/`: Directories for virtual environments used to manage dependencies in isolation from the global Python environment.

- **Distribution / Packaging**:
  - `.Python`: File created during Python installation.
  - `build/`, `develop-eggs/`, `dist/`, `downloads/`, `eggs/`, `.eggs/`, `lib/`, `lib64/`, `parts/`, `sdist/`, `var/`, `wheels/`, `*.egg-info/`, `.installed.cfg`, `*.egg`: Directories and files related to packaging and distribution of Python projects.

- **IDEs**:
  - `.idea/`: Directory created by JetBrains IDEs (like PyCharm) for project-specific settings.
  - `.vscode/.env`: VS Code-specific environment variable files.


# Script 2 

## Populating our backend

### setup.py
```bash
from setuptools import setup, find_packages

setup(name="backend", version="1.0", packages=find_packages())
```

-```setup```: This is a function that we use to define the package details and configuration for our project. In our case we have a package named 'backend', where we designated it version 1.0. 
-```packages=find_packages()```: find_packages() automatically discovers all packages and subpackages in our project directory and tells setuptools to include them in the distribution.


### config.py

Let's set up our configuration settings
First, let's set up our environment variables in the ```.env``` file.

```env
FLASK_ENV=development
DATABASE_URL=sqlite:///bots.db
```

-FLASK_ENV determines the environment in which our application will run. In this case we are in development mode.


### Configuration settings

```bash
import os
from dotenv import load_dotenv
load_dotenv()
```

The above section loads our environment variables from a .env file into the application using the python-dotenv library. Setting up our app this way helps manage sensitive data like database URLs or secret keys outside our codebase.

### Base Config:

```bash
class Config:
    ENV = os.getenv("FLASK_ENV", "development")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

This is our base configuration class from which other configurations inherit. 

- `os`: The os module in Python provides a way to interact with the underlying operating system. It enables us to perform tasks such as file manipulation, directory management, accessing environment variables and process control among other things. In our case, combining it with the getenv function allows us to safely access environment variables in our system. The getenv method retrieves the value of the environment variable provided as an argument, it returns false if the variable does not exist.
- `ENV`: Determines the environment (development, production, etc) with a default of "development".
- `SQLALCHEMY_DATABASE_URI`: Sets the database connection URL. In our case we set it to 

### Development, Testing and Production Config:

```bash
class DevelopmentConfig(Config):
    DEBUG=True
    
class TestingConfig(Config):
    TESTING=True
    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI=os.getenv("PRODUCTION_DATABASE_URL")
    
    
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig }
```

- `Testing Config`: This class sets up the configuration for testing. It enables TESTING mode, which makes Flask behave differently for example any errors encountered are raised rather than handled.
It also uses sqlite for testing purposes to avoid modifying production data.

- `Production Config`: Here, the `SQLALCHEMY_DATABASE_URI` is strictly set from the environment variable `PRODUCTION_DATABASE_URI` to ensure we use the correct production database.

- `Config Dictionary`: The dictionary allows for easy selection of configurations based on the environment. We set the default configuration to DevelopmentConfig.

## Models File

```bash
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)
```

- `Metadata`: This is a core part of SQLALchemy that holds information about the database schema. It acts as a sort of registry for tables, columns and relationships in the database. While it doesn't affect database operations directly, it is essential for keeping track of the schema structure. In this example we define a naming convention for our foreign key constraints (which we use to establish relationships between tables).

- `Foreign Key Naming convention`: The code snippet above sets up custom naming conventions for foreign key constraints in our Flask application.

`naming_convention` is a dictionary argument passed to the Metadata object that will define our custom naming conventions for database constraints.

- `%()s` is a string formatting placeholder which SQLAlchemy uses to insert specific related data dynamically. This syntax is provided by SQLAlchemy and is inspired by Python's string formatting, where % is used to substitute values into a string. In SQLAlchemy this interpolation occurs automatically when generating the database schema.

*How it works*

- `fk_`: This is the prefix we will use for all foreign key constraint names, indicating that this is a foreign key.
- `%(table_name)s`: This will be replaced with the name of the first(or only) column involved in the foreign key relationship. 
- `%(column_0_name)s`: This will be replaced with the name of the first (or only) column involved in the foreign key relationship. If there are multiple columns.
- `%(referred_table_name)s`: This will be replaced with the name of the table that the foreign key column refers to (the target table).

### Example:

- Let's assume we have a foreign key between a table `users` and another table `orders`. Using the naming convention we defined above:

- Table: `orders`
- Column: `user_id` (This is the foreign key)
- Referred Table: `users`

*The generated foreign key constraint name would be:*

`fk_orders_user_id_users`


*Why Automatic Naming is less important in SQLite*

It is important to understand that while our sqlite database does not need an explicitly defined naming convention, other large database systems like PostgreSQL require explicitly named constraints. SQLite supports foreign key constraints but does not provide an option to automatically name foreign key constraints. If you don't provide a name, SQLite will enforce the constraint without generating a name for it like other databases. SQLite internally manages foreign keys without requiring named constraints, and the foreign key rules will still be enforced. SQLite will also report errors due to foreign key constraint violations without referencing the name of the foreign key. This contrasts with other databases which might reference the constraint name in error messages. 
By us explicitly assigning names to our SQLite database foreign keys, we are setting ourselves up for good database practice when we move on to production databases like PostgreSQL.

- If we get a foreign key violation error, the error message might be as follows in SQLite and PostgreSQL:

*SQLite*
```sql
FOREIGN KEY constraint failed
```

*PostgreSQL*
```sql
ERROR: insert or update on table "orders" violates foreign key constraint "fk_orders_user_id"
```

### Tables

We are going to have three tables in our database. A User, Game and Review table.

```bash
# Begin by importing the necessary modules from Flask and SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Setting a custom naming convention for foreign key constraints
# This helps ensure that your foreign key constraints are named in a structured way.
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

# Initialize the SQLAlchemy object and pass the custom metadata
# SQLAlchemy is the ORM (Object Relational Mapper) that helps map Python objects (models) to database tables.
db = SQLAlchemy(metadata=metadata)

# The `user_games` table is an association table to represent a many-to-many relationship between Users and Games.
user_games = db.Table(
    "user_games",  # This is the table name
    db.Column("users_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),  # Foreign key referencing User
    db.Column("game_id", db.Integer, db.ForeignKey("games.id"), primary_key=True)  # Foreign key referencing Game
)

# Define the `User` class, which will be mapped to the `users` table in the database
class User(db.Model):
    __tablename__ = "users"  # Explicitly defining the table name
    
    # The `id` column is the primary key, meaning each user will have a unique identifier
    id = db.Column(db.Integer, primary_key=True)
    
    # The `username` column is unique, ensuring no two users can have the same username
    username = db.Column(db.String(55), unique=True, nullable=False)
    
    # The `games` relationship connects the User model to the Game model.
    # Using `backref` creates a bidirectional relationship; `user` will be available on the Game model.
    games = db.relationship("Game", backref="user", cascade="all, delete-orphan")
    
    # The `reviews` relationship connects the User model to the Review model.
    reviews = db.relationship("Review", backref="user")

# Define the `Game` class, which will be mapped to the `games` table
class Game(db.Model):
    __tablename__ = "games"  # Explicitly defining the table name
    
    # The `id` column is the primary key for the game
    id = db.Column(db.Integer, primary_key=True)
    
    # The `title` column stores the game's title
    title = db.Column(db.String(100), nullable=False)
    
    # The `genre` column stores the genre of the game
    genre = db.Column(db.String(55), nullable=False)
    
    # The `reviews` relationship connects the Game model to the Review model.
    reviews = db.relationship("Review", backref="game", cascade="all, delete-orphan")
    
    # The `user_id` column establishes a foreign key relationship to the `users` table.
    # This associates each game with a specific user (owner of the game).
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

# Define the `Review` class, which will be mapped to the `reviews` table
class Review(db.Model):
    __tablename__ = "reviews"  # Explicitly defining the table name
    
    # The `id` column is the primary key for the review
    id = db.Column(db.Integer, primary_key=True)
    
    # The `content` column stores the review text
    content = db.Column(db.String())
    
    # The `user_id` column establishes a foreign key relationship to the `users` table.
    # This means the review was written by a specific user.
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    # The `game_id` column establishes a foreign key relationship to the `games` table.
    # This associates each review with a specific game.
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
```


## Seed File

```bash
from src import create_app
from models import db, User, Gemstone, Review, user_gemstones
from faker import Faker
import random

# faker is a library that generates random data, from usernames to colors to addresses. This saves us time during testing by providing us with fake bur realistic data.
fake = Faker()

gemstone_names = ["Ruby", "Emerald", "Tanzanite", "Aquamarine", "Alexandrite", "Labradorite", "Diamond", "Sapphire", "Citrine", "Tsavorite", "Quartz", "Lapis Lazuli", "Opal", "Topaz"]

def create_fake_user():
    user = User(
        username=fake.user_name()
    )
    return user
    
def create_fake_gemstone():
    gem = Gemstone(
        gemstone_name=random.choice(gemstone_names),
        color=fake.color_name()
    )
    return gem

def seed():
    
    #Before adding new data, we first delete any existing data in all our tables to ensure we don't get duplicate entries. This is important when you want to reset our database and test things with a clean slate.
    db.session.query(user_gemstones).delete()
    db.session.query(User).delete()
    db.session.query(Gemstone).delete()
    db.session.query(Review).delete()
    
    
    # We create 10 fake users here by calling create_fake_user(), add them to the session, append them to the users list and commit them to the database
    users = []
    gems = []
    
    for _ in range(10):
        user = create_fake_user()
        db.session.add(user)
        users.append(user)
    db.session.commit()
    
    
    # We do the same for the gemstones.
    for _ in range(50):
        gem = create_fake_gemstone()
        db.session.add(gem)
        gems.append(gem)
    db.session.commit()
    
    
    ''' 
    *Associating Users with Gemstones and Reviews:- Here we create associations between our tables.
    * Each user is randomly assigned 1 to 5 gemstones. If a user doesn't already have the chosen gemstone, it is appended to their gemstone list.
    * For each gemstone a user owns, we create a review. The review content is generated using Faker's paragraph() method. We then assign the user_id and gemstone_id to the review to establish the relationships.
    ''' 
    for u in users:
        for _ in range(random.randint(1, 5)):
            gem = random.choice(gems)
            
            if gem not in u.gemstones:
                u.gemstones.append(gem)
                
            review = Review(
                content = fake.paragraph(),
                user_id = u.id,
                gemstone_id = gem.id
            )
            db.session.add(review)
    db.session.commit()
    
'''
* Finally, we ensure this script runs when executed directly.
* This block of code ensures that when we run this file, it initializes the Flask app, sets up the database context, and calls the seed() function to populate our database.
'''
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed()
```

## Project Initialization and the __init__.py file

```bash
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from models import db
from config import config

# We initialize Flask-Migrate but don't yet bind it to any app or database. This deferred initialization allows it to be tied to different apps if need be.
migrate = Migrate()

# The create_app function is a factory function we design to create and configure an instance of a Flask application. We pass the config_name argument so we can call the function with different configuration settings, if none is provided it defaults to "default"

def create_app(config_name="default"):
    
    # The below line app = Flask(__name__) initializes a Flask app instance. The __name__ argument is a built-in Python variable that refers to the name of the module in which it is used. When a Python script is run, the interpreter sets the __name__ variable. If the script is run directly(i.e., the main program being executed), __name__ is set to the string "__main__". If the script is imported as a module in another script, __name__ is set to the module's name(the file's name without the .py extension). So, in our case __name__ is used so Flask knows the location of our application and can locate resources like static files and templates.
    app = Flask(__name__)

    #The below line loads configuration settings  from the config object based on the environment name provided. In our case we load the database URI and set modification tracking to false.
    app.config.from_object(config[config_name])

    # Here, we bind our SQLAlchemy database instance to the Flask app. Since SQLAlchemy is initialized outside the app, it must be explicitly attached to the current app instance.
    db.init_app(app)

    # Here, we enable CORS for the entire app, allowing our app to handle cross-origin HTTP requests. This is useful if our frontend runs on a different domain or port than your Flask backend.
    CORS(app)

    # This binds Flask-Migrate to both the app and the SQLAlchemy database instance. It enables us to run database migrations to apply schema changes to our database.
    migrate.init_app(app, db)

    # This line returns the fully conigured Flask app instance.
    return app
```
- The `__init__.py` file marks the directory as a Python package. Placing our initialization code in `__init__.py` encourages modularity. This way we can have the code necessary to initialize our Flask app in this file and create multiple instances of the app in the `app.py` file depending on which environment we are in.


## The app File

```bash

# The below snippet serves as the entry point to run our Flask application.
from src import create_app

# The first line checks if the script is being run directly or imported as a module. If the file is being imported into another module, this block will not run.
if __name__ == "__main__":

    # We set the configuration name to "development". The create_app function will use this value to load the corresponding configuration from the config object (in our config.py file)
    config_name = "development"

    # This line calls the create_app function and passes the "development" configuration to it. The function returns a fully initialized Flask app instance configured for the development environment
    app = create_app(config_name)

    # This starts the Flask development server.
    # Setting the host to 0.0.0.0 tells Flask to listen on all available network interfaces. It allows our app to be accessed not just from our local machine but from other devices on the network.
    # We then specify the port number that the server will use. By default Flask uses port 5000, but here we explicitly set it to 5500.
    app.run(host="0.0.0.0", port=5500)
```