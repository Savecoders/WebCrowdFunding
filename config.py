import os
from flask import Flask, render_template
from dotenv import load_dotenv

from src.routes import user, projects

# Load the environment variables from the .env file
load_dotenv()


def create_app():
    # Create the flask app
    # search for templates and static in the templates folder
    app = Flask(__name__, template_folder='./templates',
                static_folder='./static')

    # Set up the app configuration

    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', default='dev'),
        DATABASE_HOST=os.getenv('DATABASE_HOST'),
        DATABASE_PASSWORD=os.getenv('DATABASE_PASSWORD'),
        DATABASE_USER=os.getenv('DATABASE_USER'),
        DATABASE_PORT=os.getenv('DATABASE_PORT'),
        DATABASE_DSN=os.getenv('DATABASE_DSN'),
    )
    # Create the database object
    from src.db import init_app

    init_app(app)

    # Register the blueprints
    app.register_blueprint(user.bp)
    app.register_blueprint(projects.bp)

    # app / route

    @app.route('/')
    def index():
        # use template
        return render_template('index.html', title='Home', message='Hello World!')

    return app
